"""
V5.32 lane B — the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the Espace Personnes.

What the recomposed pages promise, read in the rendered HTML and in the built sheets (the presentation was judged in
headed Chrome — C:/tmp/ile_v5_council/.work/v532-global/B/NOTES.md — and the preview's behaviour in
test_pathways_browser_v532_b.py):

* /parcours/ is «l'esploratore»: the four families as the navigation, each its pathways as rows in the prescribed
  order — a row is the link to its sheet (never a link to a sheet that is not live); no numerals, no icon tiles; one
  preview per pathway, hidden from assistive technology, its link out of the tab order; the actors a preview names are
  the ones its own sheet lists; the family-reunification pathway draws its semantic plate, never a photograph;
* a sheet carries its family (never an ordinal «n/8»), its photograph from the site's one pairing
  (pages.services.PATHWAY_FRAMES), a sticky local navigation whose anchors are the drawn chapters, the milestones
  without figures, the actors as a register with their official hosts, its neighbours of the same family;
* Diplômes and Formation: no figure in the dossier; never the mosaic — the space's pages as a register of links on
  /parcours/, which their closing band leads to;
* before gate G3 the interim index speaks the same language — its sheets loaded, the questionnaire's panel in the head,
  the sheets' notice, the two moments on the rail;
* every sheet inside its measured ceiling (gzip -9) — each lower than before — and the explorer's script inside its own.

The correction round of the senior integration review (REVIEW.md §3, 12 Nov 2026): Formation's «après l'arrivée» card
draws adult learning, the microscopes are the scientific-research pathway's alone (P1-1); the self-employment pathway
draws its own frame and the calliper stays with Entreprises (P2-1); the eight sheets, Formation and Diplômes close on
ONE compact band — the anti-fraud notice, the questionnaire's action, the way to the register —, /parcours/ alone keeps
the full trio (P2-3).
"""

from __future__ import annotations

import gzip
import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.conf import settings

pytestmark = pytest.mark.django_db

ROOT = Path(settings.BASE_DIR)
STATIC = ROOT / "static"

#: measured 12 Nov 2026 (gzip -9 of the built file), ceiling = measure + ≤ 3 % — each below its V5.22 ceiling
#: RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the correction
#: round of the senior integration review (P2-3) — the sheet's, Formation's and Diplômes' bundles shed the boussole's
#: plate and the register for ONE closing band (_chiusura.css); their ceilings come down with them (stronger), measure
#: + ≤ 3 % again
CEILINGS = {
    # re-measured at integration (7ff0074d): the explorer plate's rule in cascade order, the closing band's one-measure
    # sentence flow — ceilings unchanged, each still measure + ≤ 3 %
    "css/dist/pathways/index.css": 9_000,  # measured 8 928 (8 890 at lane B; 8 894 before the plate's flat tint; was 9 864)
    "css/dist/pathways/sheet.css": 8_648,  # measured 8 473 (8 420 at lane B; 8 470 before P2-3; was 9 186)
    "css/dist/pathways/diplomas.css": 8_229,  # measured 8 048 (7 990 at lane B; 8 232 before P2-3; was 8 717)
    "css/dist/pathways/training.css": 7_850,  # measured 7 677 (7 622 at lane B; 7 905 before P2-3; was 8 353)
    "js/dist/esplora.js": 533,  # measured 518 (new)
}


def _gz(relative: str) -> int:
    return len(gzip.compress((STATIC / relative).read_bytes(), 9))


def _main(html: str) -> BeautifulSoup:
    return BeautifulSoup(html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0], "html.parser")


@pytest.fixture
def get(client, seeded, phase3_open, legal_published):
    def fetch(path: str) -> str:
        response = client.get(path)
        assert response.status_code == 200, (path, response.status_code)
        return response.content.decode("utf-8")

    return fetch


def test_the_space_s_sheets_and_the_explorer_s_script_stay_inside_their_measured_ceilings():
    for relative, ceiling in CEILINGS.items():
        assert _gz(relative) <= ceiling, (relative, _gz(relative), ceiling)


def test_the_sheet_s_photograph_stands_on_the_head_print_written_in_tokens():
    """The integration review's addendum (test_design_docs: an app sheet reads the design tokens only, DS 2026 §2.1):
    the sheet's photograph keeps the head print of v5/_fronte.css — its recipe written in tokens in _scheda.css, never
    the partial's private name — and the two recipes stay one; the semantic plate is one flat tint, no gradient."""
    fronte = re.sub(r"/\*.*?\*/", "", (STATIC / "css" / "v5" / "_fronte.css").read_text(encoding="utf-8"), flags=re.S)
    print_recipe = " ".join(re.search(r"--fronte-print:\s*([^;]+);", fronte).group(1).split())
    pathways = ROOT / "apps" / "pathways" / "static" / "pathways"
    scheda = re.sub(r"/\*.*?\*/", "", (pathways / "_scheda.css").read_text(encoding="utf-8"), flags=re.S)
    photograph = re.search(r"(?m)^\.scheda-foto \{([^}]*)\}", scheda).group(1)
    assert " ".join(re.search(r"box-shadow:\s*([^;]+);", photograph).group(1).split()) == print_recipe
    for name in ("_scheda.css", "_esplora.css"):
        source = re.sub(r"/\*.*?\*/", "", (pathways / name).read_text(encoding="utf-8"), flags=re.S)
        assert "gradient(" not in source and "var(--fronte-print)" not in source, name


def test_the_retired_compositions_leave_the_space_s_sheets():
    for name in ("index", "sheet", "diplomas", "training"):
        source = (ROOT / "apps" / "pathways" / "static" / "pathways" / f"{name}.css").read_text(encoding="utf-8")
        for gone in ("_sec-tracciato", "_sec-mosaico", "_persone-v2", "_sec-filo", "_sec-indice", "_index.css"):
            assert gone not in source, (name, gone)
    assert not (ROOT / "apps" / "pathways" / "static" / "pathways" / "_index.css").exists()


def test_the_explorer_holds_the_eight_pathways_by_family_in_the_prescribed_order(get):
    from pathways import services

    main = _main(get("/fr/parcours/"))
    explorer = main.select_one("[data-esplora]")
    assert explorer is not None
    families = [f["data-family"] for f in explorer.select(".esplora__famiglia")]
    assert families == [family for family, _keys in services.PATHWAY_FAMILIES]
    rows = explorer.select(".esplora__voce")
    keys = [row["data-pathway"] for row in rows]
    prescribed = [entry.key for entry in services.index_entries()]
    for family, members in services.PATHWAY_FAMILIES:
        assert [k for k in keys if k in members] == [k for k in prescribed if k in members]
    assert sorted(keys) == sorted(prescribed)
    for row in rows:
        link = row.select_one("a.esplora__link")
        assert link is not None and link["href"].endswith(f"/parcours/{row['data-pathway']}/")
        # no numeral, no icon tile: the order is the rows'
        assert not row.select(".sez-tile, .tracciato__num")
        assert not re.search(r"\b0?[1-8]\b", row.select_one(".esplora__titolo").get_text())


def test_the_preview_is_for_the_eye_and_names_only_the_sheet_s_own_actors(get):
    from pathways import services
    from pathways.models import Pathway

    main = _main(get("/fr/parcours/"))
    panel = main.select_one(".esplora__anteprime")
    assert panel["aria-hidden"] == "true"
    previews = panel.select("[data-esplora-anteprima]")
    assert len(previews) == 8
    assert [p.has_attr("hidden") for p in previews] == [False] + [True] * 7
    for preview in previews:
        for link in preview.select("a"):
            assert link["tabindex"] == "-1"
        row = Pathway.objects.get(key=preview["data-esplora-anteprima"])
        named = [li.get_text(strip=True) for li in preview.select(".esplora__attori-lista li")]
        assert named == [a["name"] for a in services.authorities(row, "fr")]
    family = panel.select_one("[data-esplora-anteprima='family_reunification']")
    assert family.select_one(".esplora__foto--piastra") and not family.select("img")


def test_no_numbered_how_it_works_and_no_mosaic_on_the_space_s_pages(get):
    for path in ("/fr/parcours/", "/fr/diplomes-et-titres/", "/fr/formation/"):
        main = _main(get(path))
        assert not main.select(".mosaico, .mosaico__tessera"), path
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the
    # correction round of the senior integration review (P2-3) — the space's register of links stands once, whole, on
    # /parcours/ (its anchor the one the closing band leads to); Diplômes and Formation reach it from «la chiusura»
    register = _main(get("/fr/parcours/")).select_one("section#espace-personnes .spazio__voci")
    assert register is not None and len(register.select("a.spazio__voce")) >= 4
    for path in ("/fr/diplomes-et-titres/", "/fr/formation/"):
        main = _main(get(path))
        assert not main.select(".spazio__voci"), path
        assert main.select_one('.chiusura a[href="/fr/parcours/#espace-personnes"]'), path
    index = _main(get("/fr/parcours/"))
    assert not index.select(".come__num")
    assert all(not p.get_text(strip=True) for p in index.select(".come__punto"))
    diplomas = _main(get("/fr/diplomes-et-titres/"))
    assert all(not n.get_text(strip=True) for n in diplomas.select(".dossier__num"))


def test_a_sheet_names_its_family_its_photograph_and_its_neighbours(get):
    from pages.services import PATHWAY_FRAMES
    from pathways import services

    for entry in services.index_entries():
        main = _main(get(f"/fr/parcours/{entry.key}/"))
        label = main.select_one("header.ingresso .ingresso__label").get_text(" ", strip=True)
        assert "/8" not in label and str(services.FAMILY_LABELS[entry.family]) in label
        frame = main.select_one("header.ingresso .ingresso__aside")
        if entry.key in PATHWAY_FRAMES:
            img = frame.select_one("img")
            assert img is not None and img["fetchpriority"] == "high" and img["alt"], entry.key
        else:
            assert frame.select_one(".scheda-foto--piastra") and not frame.select("img"), entry.key
        siblings = [a["href"] for a in main.select(".scheda-vicini a.scheda-vicino") if "/parcours/" in a["href"]]
        members = dict(services.PATHWAY_FAMILIES)[entry.family]
        expected = [f"/fr/parcours/{k}/" for k in members if k != entry.key]
        assert [h for h in siblings if h in expected] == expected, entry.key
        assert f"/fr/parcours/{entry.key}/" not in siblings


def test_the_sheet_s_navigation_names_the_drawn_chapters_and_its_milestones_carry_no_figure(get):
    main = _main(get("/fr/parcours/salaried_work/"))
    nav = main.select_one("nav.scheda-nav[data-sec-js~='spia']")
    anchors = [a["href"].lstrip("#") for a in nav.select("a.scheda-nav__voce")]
    assert anchors and all(main.select_one(f"section#{anchor}") for anchor in anchors)
    steps = main.select(".scheda-tappa")
    assert len(steps) == 5
    for step in steps:
        assert not step.select_one(".scheda-tappa__punto").get_text(strip=True)
    # the one milestone a page of the space answers: preparing before departure → Formation
    links = [a["href"] for a in main.select(".scheda-tappa__via a")]
    assert links == ["/fr/formation/"]


def test_the_actors_are_a_register_with_their_official_hosts_and_the_platform_stands_outside_it(get):
    main = _main(get("/fr/parcours/salaried_work/"))
    register = main.select_one("#autorites .scheda-attori__lista")
    assert register is not None
    assert "Italy Legal Entry" not in register.get_text()
    assert "Italy Legal Entry" in main.select_one("#autorites .scheda-attori__nota").get_text()
    for link in register.select("a.autorita"):
        assert link["href"].startswith("https://")
        host = link.find_next_sibling(class_="autorita__host")
        assert host is not None and host.get_text(strip=True) in link["href"]


def test_the_interim_index_speaks_the_open_page_s_language(client, seeded, legal_published, before_phase3):
    """Before gate G3 the Parcours index is its interim page (pathways/index_interim.html): it loads the space's sheets
    and draws the open page's head, notice band and rail — the regression a review caught once (the interim page lost
    every style when the route board's sheet left) is held here, in the rendered HTML."""
    for lang in ("fr", "ar"):
        html = client.get(f"/{lang}/parcours/").content.decode("utf-8")
        assert "page-pathways--interim" in html, lang
        head = BeautifulSoup(html.split("</head>", 1)[0], "html.parser")
        sheets = [link["href"] for link in head.select('link[rel="stylesheet"]')]
        assert any(s.endswith("css/dist/pathways/index.css") for s in sheets), (lang, sheets)
        assert any(s.endswith("css/dist/pages/css/fronte.css") for s in sheets), (lang, sheets)
        main = _main(html)
        # the questionnaire's panel in the head's seat — the door's way in, the page's one primary action
        way = main.select_one("header.ingresso .ingresso__aside > .esplora-via.via.ingresso__way")
        assert way is not None and way.select_one(f'.via__action a.btn--primary[href="/{lang}/orientation/"]'), lang
        assert len(main.select(".btn--primary")) == 1, lang
        # the sheets' notice where the explorer will stand, its help line beside it; the two moments on the rail
        assert main.select_one('section.esplora-attesa[data-ground="paper"][data-rhythm="strip"] .aiuto a.email')
        rings = main.select(
            'section.esplora-come#orientation .come__tappe[data-steps="2"] > li.come__tappa > .come__punto'
        )
        assert len(rings) == 2 and all(r.get("aria-hidden") == "true" and not r.get_text(strip=True) for r in rings)
        assert not main.select(".come__num, .sez-tile, .mosaico, .esplora__voce"), lang


# ---------------------------------------------- the correction round of the senior integration review (12 Nov 2026)


def _templates() -> list[Path]:
    return [*(ROOT / "templates").rglob("*.html"), *(ROOT / "apps").rglob("templates/**/*.html")]


def test_formation_s_after_card_shows_adult_learning_and_the_microscopes_are_research_s_alone(get):
    """P1-1: «après l'arrivée» (Italian, civic education, safety at work, a qualification) draws a class for adults — a
    trainer at a flipchart before seated participants, all seen from behind — never the row of microscopes, which is
    the scientific-research pathway's frame alone: its own slot, drawn only through the one pairing."""
    from pages import imagery
    from pages.services import PATHWAY_FRAMES

    after, research = imagery.BY_KEY["training.after"], imagery.BY_KEY["pathways.research"]
    assert [key for key, (slot, _v) in PATHWAY_FRAMES.items() if slot == research.key] == ["scientific_research"]
    assert not [t for t in _templates() if f'"{research.key}"' in t.read_text(encoding="utf-8")]
    formation = get("/fr/formation/")
    img = _main(formation).select_one('figure[data-slot="training.after"] img')
    assert img is not None and f"/img/v5/{after.family}/{after.slug}-" in img["src"]
    assert research.slug not in formation
    head = _main(get("/fr/parcours/scientific_research/")).select_one("header.ingresso .ingresso__aside img")
    assert f"/img/v5/{research.family}/{research.slug}-" in head["src"]


def test_the_self_employment_pathway_draws_its_own_frame_and_the_calliper_stays_with_entreprises(get):
    """P2-1: the self-employment pathway draws its own frame — a shoemaker at his bench, seen from above — on its sheet,
    in the explorer's row and preview and in the home's stage (the one pairing); the Entreprises landing's calliper
    has no rendering for another page and no pathway draws it."""
    from pages import imagery
    from pages.services import PATHWAY_FRAMES

    own, calliper = imagery.BY_KEY["pathways.independent"], imagery.BY_KEY["companies.hero"]
    drawn_by = [key for key, (slot, _v) in PATHWAY_FRAMES.items() if slot == own.key]
    assert drawn_by == ["self_employment_entrepreneurship"]
    assert calliper.variants == () and calliper.key not in {slot for slot, _v in PATHWAY_FRAMES.values()}
    assert not [t for t in _templates() if f'"{own.key}"' in t.read_text(encoding="utf-8")]
    path = f"/img/v5/{own.family}/{own.slug}-"
    sheet = get("/fr/parcours/self_employment_entrepreneurship/")
    assert path in _main(sheet).select_one("header.ingresso .ingresso__aside img")["src"]
    index = get("/fr/parcours/")
    explorer = _main(index)
    for selector in (
        ".esplora__voce[data-pathway='self_employment_entrepreneurship'] img",
        "[data-esplora-anteprima='self_employment_entrepreneurship'] img",
    ):
        assert path in explorer.select_one(selector)["src"], selector
    home = get("/fr/")
    assert path in home
    for html in (sheet, index, home):
        assert calliper.slug not in html
    assert calliper.slug in get("/fr/entreprises/")


def test_the_two_frames_hold_what_their_full_resolution_check_found():
    """Each frame was looked at whole before it entered (B/NOTES.md): its crop and its one redaction keep what was
    found — nobody identifiable, no door, no legible writing, no lit screen — and its alt is a concrete sentence."""
    from pages import imagery

    def frame(key: str):
        rec = imagery.record(imagery.BY_KEY[key])
        (crop,) = rec["crops"]
        (mark,) = rec["redactions"]
        cx0, cy0, cx1, cy1 = crop["crop_fraction"]
        rx0, ry0, rx1, ry1 = mark["box_fraction"]
        # one box, erased by the median mode (a blur would read as a patch), inside the crop it cleans
        assert mark["mode"] == "median" and cx0 <= rx0 < rx1 <= cx1 and cy0 <= ry0 < ry1 <= cy1, (key, mark)
        return crop["crop_px"], rec["original_px"], mark["reason"]

    # the class: the glazed door with blinds at the frame's left edge (it ends at x 0.11) stays outside; the participants
    # are seen from behind; the handwritten word on the flipchart is erased
    box, (w, _h), reason = frame("training.after")
    assert box[0] >= 0.12 * w and "handwritten" in reason, (box, reason)
    # the shoemaker: the crop starts under his chin (his face, seen from above, ends at y 0.215); the lit phone is erased
    box, (_w, h), reason = frame("pathways.independent")
    assert box[1] >= 0.22 * h and "phone" in reason, (box, reason)
    for key in ("training.after", "pathways.independent"):
        alt = str(imagery.BY_KEY[key].alt)
        assert 30 <= len(alt) <= 200 and alt[0].isupper() and not alt.endswith("."), (key, alt)


def test_the_space_s_pages_close_on_one_compact_band_and_parcours_keeps_the_full_trio(get):
    """P2-3: the anti-fraud band, the «Dans l'Espace Personnes» register and the questionnaire's plate ended eleven
    pages, so two sheets read one after the other ended alike. The eight sheets, Formation and Diplômes close on ONE band
    (pathways/_chiusura.html): the anti-fraud notice whole — its locked title and body, by the one component that
    renders them —, the questionnaire's caution and its one primary, the way to the space's register, the help line;
    nothing of the trio stands elsewhere on those pages. /parcours/ keeps the full trio."""
    from cms import locked_content
    from pathways import services

    body = locked_content.text("p3.antifraud.body", "fr")
    pages = [f"/fr/parcours/{entry.key}/" for entry in services.index_entries()]
    assert len(pages) == 8
    for path in (*pages, "/fr/formation/", "/fr/diplomes-et-titres/"):
        main = _main(get(path))
        bands = main.select('[data-action="orientation"]')
        assert len(bands) == 1, path
        band = bands[0]
        # the page's last part: the sheet's last chapter, Formation's and Diplômes' last band (on «pietra»)
        if path in pages:
            assert band is main.select(".scheda-capitoli > section.scheda-cap")[-1] and band["id"] == "avertissements"
        else:
            assert band is main.select("section.sez")[-1] and band["data-ground"] == "pietra", path
        notice = band.select_one("aside.protezione[data-callout='antifraud']")
        assert " ".join(notice.select_one('[data-locked="p3.antifraud.body"]').get_text(" ").split()) == body, path
        step = band.select_one(".chiusura__seguito")
        assert "Les décisions relèvent des autorités compétentes." in step.get_text(" "), path
        assert [a["href"] for a in step.select("a.btn--primary")] == ["/fr/orientation/"], path
        assert step.select_one('a.link-arrow[href="/fr/parcours/#espace-personnes"]'), path
        assert step.select_one(".sez-annotation a.email[href^='mailto:']"), path
        # the trio once, in that band: one notice, no register, no plate, no «Orientation» chapter, one primary
        assert len(main.select("aside.protezione")) == 1, path
        assert not main.select(".spazio, .spazio__voci, .boussole, #orientation"), path
        assert len(main.select(".btn--primary")) == 1, path
    index = _main(get("/fr/parcours/"))
    assert index.select_one("section.spazio#espace-personnes .spazio__voci a.spazio__voce")
    assert index.select_one("section.persone-protezione aside.protezione[data-callout='antifraud']")
    assert index.select_one("header.ingresso .ingresso__aside a.btn--primary[href='/fr/orientation/']")
    assert not index.select(".chiusura")


def test_the_closing_band_is_one_partial_in_the_three_sheets_that_draw_it():
    """P2-3: «la chiusura» is pathways/_chiusura.css in the sheet, Formation's and Diplômes' bundles; the plate's partial
    leaves them, the register's stays with /parcours/ alone, and the anti-fraud notice reaches the three pages through
    the band's partial only."""
    for name in ("index", "sheet", "diplomas", "training"):
        source = (ROOT / "apps" / "pathways" / "static" / "pathways" / f"{name}.css").read_text(encoding="utf-8")
        assert ('@import url("_chiusura.css");' in source) is (name != "index"), name
        assert ('@import url("_spazio.css");' in source) is (name == "index"), name
        assert "_sec-boussole.css" not in source, name
    for name in ("detail", "diplomas", "training"):
        source = (ROOT / "templates" / "pathways" / f"{name}.html").read_text(encoding="utf-8")
        assert source.count('{% include "pathways/_chiusura.html"') == 1, name
        # no include of the plate's or the register's partial (the comments keep their history)
        assert '{% include "components/sezioni/boussole.html"' not in source, name
        assert '{% include "pathways/_spazio.html"' not in source, name
        assert '{% include "components/sezioni/protezione.html"' not in source, name
