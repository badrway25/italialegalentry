"""
V5.22 — HOMEPAGE COMPOSITION V2 (SECTION_SYSTEM_V2 §3.1, §9.3; lane H): the home's sections composed from the library.

What this module holds, without a browser (the browser half is test_home_browser_v522_h.py):
* every section under the hero is a V2 section — its pattern, its ground, its rhythm, its head — and two grounds of one
  kind never touch, whatever order the back office gives the sections;
* the hand-off: the hero's line beside its statement, and its continuation in the orientation's band;
* the orientation's route, the pathways' index and stage, the trust plates' own FAQ entries, in both gate states;
* the pilot's lead says what its panel shows — and the seed brings an untouched old default to it, never an editor's;
* the home's page-only sheets and their ceilings (SECTION_SYSTEM_V2 §7.1), main.css untouched;
* round 1 (QA_ROUND1, label v522-h-improve1): the hand-off computed once, the trust answers as one tablet with its
  plinth, the closed gate's families on the index's tiles, the stage's languages of parts, the pilot's two shores kept
  together, the reserved key beside its button and in the identity's gold, the ecosystem's doorway drawn around its
  photograph, the Arabic page's own rules;
* round 2 (QA_ROUND2, label v522-h-improve2): the stage's way to its sheet in the page's language (the catalogue's
  «Consulter la page du parcours»), the tablet's bond named by its fields (a rule Blink files under a class);
* final fix round (QA_ROUND3, label v522-h-fix): every line the home draws with the verb «stroke» carries its dash in
  its drawing's user space — the doorway's and the phone doors' lines through their own masks, never a dash on a
  non-scaling stroke (laid in device pixels); the Arabic index's titles set against their glyphs; the colophon's
  connector on its folio's rule;
* after the final review (v522-h-final-qa1, label v522-h-final-improve): the pilot's French title on the Arabic page
  takes its seam's alignment (F-M1), its lead never ends on one word (F-m2), the closed gate's two plates stand at their
  own heights (F-m1), and the home's sheets read the input's modality in one rule (F-M2, lane H's share).
"""

from __future__ import annotations

import gzip
import re
from pathlib import Path

import pytest
from django.conf import settings

from cms import locked_content
from core import icons
from pages import content, seeds, services
from pages.models import HomeSection, SectionKey
from pages.tests.conftest import escaped, section_order, text_of

pytestmark = pytest.mark.django_db

ROOT = Path(settings.BASE_DIR)
DIST = ROOT / "static" / "css" / "dist"
OLD_PILOT_LEAD = "Des besoins des entreprises au suivi : la séquence du projet pilote, étape par étape."


def _block(html: str, key: str) -> str:
    """A section of the home, from its opening tag to the next section of the page (nested sections included)."""
    head, sep, rest = html.partition(f'data-section="{key}"')
    assert sep, key
    return rest.split("data-section=", 1)[0]


def _sections(html: str) -> list[dict]:
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    out = []
    for tag in re.findall(r"<section class=\"sez [^>]*>", main):
        attrs = dict(re.findall(r'([a-z-]+)="([^"]*)"', tag))
        out.append(attrs)
    return out


# ---------------------------------------------------------------------------------------------- the system


@pytest.mark.parametrize("state", ["closed", "open"])
def test_every_section_under_the_hero_is_a_v2_section_and_no_two_grounds_of_one_kind_touch(
    request, page, seeded, state
):
    if state == "open":
        request.getfixturevalue("phase3_open")
    _response, html = page("/fr/")
    sections = _sections(html)
    keys = [s["data-section"] for s in sections]
    assert keys == [k for k in section_order(html) if k not in ("hero", "banner")], keys
    for s in sections:
        assert s["data-ground"] in {"paper", "stone", "brand", "night", "photo"}, s
        assert s["data-rhythm"] in {"strip", "band", "moment"}, s
        label = s["aria-labelledby"]
        assert re.search(rf'<h2 [^>]*id="{label}"', html), (s["data-section"], "its head names it")
    grounds = ["paper"] + [s["data-ground"] for s in sections]  # the hero's wall first
    for before, after in zip(grounds, grounds[1:]):
        assert before != after, grounds
    # one brand wash a page, and one moment, placed second or third below the header on desktop (§1 rule 5)
    assert grounds.count("brand") == 1
    if state == "open":
        assert [s["data-section"] for s in sections if s["data-rhythm"] == "moment"] == ["pilot"]


def test_the_grounds_hold_when_the_back_office_reorders_or_adds_a_section(page, seeded, phase3_open, article_factory):
    """The news between «la protezione» (stone) and the promoter (paper) would set two papers side by side: the promoter
    takes the stone; an editor who moves the pathways right under the hero gives them the stone under the paper wall."""
    article_factory("Programme du Forum publié")
    _response, html = page("/fr/")
    by_key = {s["data-section"]: s["data-ground"] for s in _sections(html)}
    assert (by_key["antifraud"], by_key["news"], by_key["ecosystem"]) == ("stone", "paper", "stone"), by_key
    HomeSection.objects.filter(key__in=[SectionKey.ENTRANCES, SectionKey.ORIENTATION]).update(is_enabled=False)
    _response, html = page("/fr/")
    assert _sections(html)[0]["data-section"] == "pathways"
    assert _sections(html)[0]["data-ground"] == "stone", "never paper under the hero's paper wall"


def test_the_grounds_resolver_flips_only_the_two_light_grounds():
    views = [
        services.SectionView(key=key, template="", anchor="")
        for key in (SectionKey.HERO, SectionKey.PATHWAYS, SectionKey.NEWS, SectionKey.PILOT, SectionKey.RESERVED)
    ]
    services._grounds(views)
    assert [v.ground for v in views[1:]] == ["stone", "paper", "night", "night"]


# ---------------------------------------------------------------------------------------------- H0, S2


@pytest.mark.parametrize("state", ["closed", "open"])
def test_the_hero_line_leaves_the_statement_and_runs_on_into_the_orientation_route(request, page, seeded, state):
    if state == "open":
        request.getfixturevalue("phase3_open")
    _response, html = page("/fr/")
    hero = html.split('data-section="hero"', 1)[1].split("</section>", 1)[0]
    # beside the statement, after it: a decorative line the section runtime draws once (§2.0, the verb draw-y)
    assert re.search(
        r'</p><span class="he__soglia" data-sec="soglia" aria-hidden="true">'
        r'<span class="he__soglia-linea" data-verb="draw-y"></span></span>',
        hero,
    )
    block = _block(html, "orientation")
    capo = block.split('<div class="orienta__capo">', 1)[1].split('<div class="linea-v2', 1)[0]
    assert '<span class="orienta__soglia" data-verb="draw-y" aria-hidden="true"></span>' in capo
    # the route's origin is the T1 seal of orientation: the line turns into its sill
    route = block.split('<div class="linea-v2', 1)[1]
    first_station = route.split('<li class="linea__step', 2)[1]
    assert 'data-mark="ile-orienta"' in first_station


def test_the_orientation_route_is_the_locked_sentence_cut_and_said_once(page, seeded, phase3_open):
    from pathways.services import how_it_works

    cut = how_it_works("fr")
    data = services.build_orientation(services.BuildContext(request=None, lang="fr", phase3=True))
    assert [s["label"] for s in data["stations"]] == list(cut.steps)
    assert [s["glyph"] for s in data["stations"]] == list(icons.HOW_STEP)
    assert data["whole"] == locked_content.text("p3.persons.how_it_works", "fr")
    _response, html = page("/fr/")
    block = _block(html, "orientation")
    assert block.count(escaped(cut.caveat)) == 2, "the caveat: drawn once at the route's end, said once in the whole"
    assert 'class="btn btn--primary" href="/fr/orientation/" data-azione>' in block, "the call takes the arrival"


def test_the_orientation_route_in_another_language_carries_the_french_it_is_cut_from(page, seeded, phase3_open):
    _response, html = page("/ar/")
    block = _block(html, "orientation")
    assert re.search(r'<p class="visually-hidden" lang="fr">', block), "the whole sentence, in French, said once"
    assert re.search(r'<ol class="linea linea--large linea--across"[^>]* lang="fr" aria-hidden="true"', block)
    assert '<p class="orienta__avvertenza" aria-hidden="true" lang="fr">' in block


def test_the_orientation_gate_closed_ends_on_the_editorial_note(page, seeded):
    _response, html = page("/fr/")
    block = _block(html, "orientation")
    assert '<div class="linea__terminale"><p class="orienta__avvertenza">' in block
    assert "pré-évaluation à caractère informatif" in block.split('class="linea__terminale"', 1)[1]
    assert block.count("data-azione>Commencer le questionnaire d’orientation</a>") == 1


# ---------------------------------------------------------------------------------------------- S3


def test_the_pathways_stage_links_a_published_sheet_and_only_that(page, seeded, phase3_open):
    from pathways import services as pathway_services

    _response, html = page("/fr/")
    block = _block(html, "pathways")
    for entry in pathway_services.index_entries():
        anchor = f"parcours-{entry.key.replace('_', '-')}"
        panel = block.split(f'<section class="indice__pannello" id="{anchor}"', 1)[1].split("</section>", 1)[0]
        # round 2 (QA_ROUND2, institutional quality on it/en/ar; V5.20 strict rule — SECTION_SYSTEM_V2 §1 rule 6,
        # the language of parts): the way to the sheet is the product's own words for it, the orientation result's
        # «Consulter la page du parcours», a msgid the it/en/ar catalogues already hold (never a fallback)
        if entry.url:
            assert f'href="{entry.url}" aria-describedby="{anchor}-title">Consulter la page du parcours</a>' in panel
        else:
            assert "Consulter la page du parcours" not in panel, entry.key
    assert block.count('class="home-pathways__more"') == 1, "the space, named once at the section's foot"
    assert 'data-sec-js="indice"' in block, "the index loads its one module"


# ---------------------------------------------------------------------------------------------- S4


def test_the_pilot_lead_says_what_the_panel_shows(page, seeded, phase3_open):
    assert services.str_source(content.SECTION_DEFAULTS_BY_KEY[SectionKey.PILOT].intro) == (
        "Le même geste, sur le cèdre et sur le marbre : deux savoir-faire, deux rives, un même projet."
    )
    _response, html = page("/fr/")
    block = _block(html, "pilot")
    assert "Le même geste, sur le cèdre et sur le marbre" in block
    assert OLD_PILOT_LEAD not in html and "étape par étape" not in block
    # the panel: two panels of lane M's re-crops, developing, the thread in the seam; one link; nothing ranked
    assert block.count('data-slot="home.pilot.') == 2 and block.count('data-grade="bw-scroll"') == 2
    assert "2x3-" in block, "the full-height 2:3 panels (variant «pannello»)"
    assert block.count('class="pilota__filo') == 2 and 'class="panorama__cucitura' in block


def test_the_seed_brings_an_untouched_old_lead_to_the_new_one_and_never_touches_an_editors(db):
    seeds.seed_home_sections()
    HomeSection.objects.filter(key=SectionKey.PILOT).update(intro_fr=OLD_PILOT_LEAD)
    seeds.seed_home_sections()
    new = services.str_source(content.SECTION_DEFAULTS_BY_KEY[SectionKey.PILOT].intro)
    assert HomeSection.objects.get(key=SectionKey.PILOT).intro_fr == new
    HomeSection.objects.filter(key=SectionKey.PILOT).update(intro_fr="Un texte écrit par la rédaction.")
    seeds.seed_home_sections()
    assert HomeSection.objects.get(key=SectionKey.PILOT).intro_fr == "Un texte écrit par la rédaction."


# ---------------------------------------------------------------------------------------------- S5, S6


def test_each_trust_plate_opens_its_own_faq_entry(page, seeded, phase3_open, client):
    _response, html = page("/fr/")
    block = _block(html, "trust")
    hrefs = re.findall(r'<a class="strato__link sez-stretch" href="([^"]+)">', block)
    assert hrefs == [f"/fr/faq/#{key}" for key in content.TRUST_FAQ_KEYS]
    faq = client.get("/fr/faq/").content.decode("utf-8")
    for key in content.TRUST_FAQ_KEYS:
        assert f'id="{key}"' in faq, (key, "the FAQ keeps the permalink the plate opens")
    # the band's ground: the masonry frame, decorative, under its veil, drifting (M22)
    assert re.search(r'<div class="strato__fondo integrita__fondo" data-parallax aria-hidden="true"><figure', block)
    assert 'data-slot="home.integrity.stone"' in block and 'alt=""' in block


def test_the_warning_closes_the_band_with_the_one_plate_of_every_page(page, seeded, phase3_open):
    _response, html = page("/fr/")
    assert section_order(html).index("antifraud") == section_order(html).index("trust") + 1
    block = _block(html, "antifraud")
    assert block.count('<aside class="protezione sez-plate sez-plate--raised"') == 1
    assert 'aria-labelledby="protezione-title-home"' in html and 'id="protezione-title-home"' in block
    assert text_of("p3.antifraud.title") in block


# ---------------------------------------------------------------------------------------------- S7, S8


def test_the_promoter_stands_beside_the_working_table_under_the_arch(page, seeded, phase3_open):
    _response, html = page("/fr/")
    block = _block(html, "ecosystem")
    assert '<div class="campata campata--start campata--wide campata--arch">' in block
    assert 'data-slot="home.ecosystem"' in block and "4x3-" in block, "lane M's 4:3 re-crop under the arch"
    assert '<span class="fronte__name" lang="it" dir="ltr">AGAMI</span>' in block
    for keyword in ("depuis 2011", "Italie–Maroc"):
        assert f'<span class="em-keyword">{keyword}</span>' in block, keyword
    assert block.count('class="btn btn--secondary"') == 1


def test_the_reserved_row_turns_its_key_on_its_own_button(page, seeded, phase3_open):
    _response, html = page("/fr/")
    block = _block(html, "reserved")
    assert 'class="sez home-reserved on-inverse"' in html
    assert block.count('class="sg-g sg-g--key"') == 1, "the key's group turns about its bow (v5/_sezioni.css)"
    assert re.search(r'<a class="btn btn--secondary home-reserved__button" href="[^"]+" data-azione>', block)


# ---------------------------------------------------------------------------------------------- sheets, budgets


def _gz(path: Path) -> int:
    return len(gzip.compress(path.read_bytes(), 9))


def test_the_home_sheets_are_page_only_and_under_their_ceilings():
    """SECTION_SYSTEM_V2 §7.1: pages.css ≤ 12 288, hero.css ≤ 11 264 (H0 only), main.css never above 32 718 B gzip -9;
    the home's partial «la casa» and the library's pattern partials are imported by the home's sheet, never by
    main.css."""
    assert _gz(DIST / "pages" / "css" / "pages.css") <= 12_288
    assert _gz(DIST / "pages" / "css" / "hero.css") <= 11_264
    assert _gz(DIST / "main.css") <= 32_718
    source = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    for partial in (
        "_sezioni",
        "_sigillo",
        "_linea-v2",
        "_sec-passaggio",
        "_sec-indice",
        "_sec-strato",
        "_sec-campata",
        "_casa",
    ):
        assert f'@import url("../../css/v5/{partial}.css");' in source, partial
    main = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
    assert "_casa" not in main and "_sezioni" not in main
    casa = (ROOT / "static" / "css" / "v5" / "_casa.css").read_text(encoding="utf-8")
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(", re.sub(r"/\*.*?\*/", "", casa, flags=re.S)), "tokens only"


def test_the_home_moves_nothing_of_its_own_and_spends_its_gold_on_three_things():
    """The home's sheets animate nothing (every entrance is a verb of v5/_reveal.css); gold in the home's body is the
    pilot's thread (the hero's light continued), the orientation's arrival (the stepper's own) and the key's identity
    (§4.5) — nothing else."""
    sheet = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    code = re.sub(r"/\*.*?\*/", "", sheet, flags=re.S)
    assert "animation" not in sheet and "@keyframes" not in code
    gold = re.findall(r"var\((--(?:identity-light|identity-key|p-oro-300|he-gold[a-z-]*))\)", code)
    assert sorted(set(gold)) == ["--identity-key", "--identity-light"], gold
    lines = [line for line in code.splitlines() if "--identity-light" in line or "--identity-key" in line]
    assert len(lines) == 3, lines  # the two threads of the seam, the cedar–marble level seam, the key


# ---------------------------------------------------------------------------------------------- round 1 (QA_ROUND1)


def _hand_off(*keys):
    views = [services.SectionView(key=key, template="", anchor="", data={}) for key in keys]
    services._hand_off(views)
    return next(v.data.get("soglia") for v in views if v.key == SectionKey.ORIENTATION)


def test_the_orientation_takes_the_hero_s_line_only_right_after_the_hero():
    """M1 a: the band follows the statement and the line runs on into the route only where the orientation comes right
    after the hero — the phone's doors between them excepted; a banner, or any section, between them breaks the hand."""
    hero, doors, route = SectionKey.HERO, SectionKey.ENTRANCES, SectionKey.ORIENTATION
    banner, pathways = SectionKey.BANNER, SectionKey.PATHWAYS
    assert _hand_off(hero, route, pathways) is True
    assert _hand_off(hero, doors, route, pathways) is True
    assert _hand_off(hero, banner, doors, route) is False
    assert _hand_off(hero, doors, banner, route) is False
    assert _hand_off(hero, pathways, route) is False
    assert _hand_off(route, hero) is False


def test_the_hand_off_class_marks_the_band_that_takes_the_line(page, seeded, phase3_open):
    _response, html = page("/fr/")
    assert re.search(r'<section class="sez sez--linea home-orientation home-orientation--soglia" ', html)
    # the needle's north half: the page's one gradient, decorative
    block = _block(html, "orientation")
    assert block.count('id="orienta-ago"') == 1
    portico = re.search(r'<svg class="orienta__portico"[^>]*>(.*?)</svg>', block)
    assert 'aria-hidden="true"' in portico.group(0) and '<linearGradient id="orienta-ago"' in portico.group(1)


def test_the_trust_answers_are_one_tablet_set_in_the_wall_with_its_plinth(page, seeded, phase3_open):
    """M1 (trust): «four equal white cards» become ONE raised plate — four fields in the masonry's running bond, the way
    to every question its plinth inside it; each field still opens its own FAQ entry; the plate settles once (depth)."""
    _response, html = page("/fr/")
    block = _block(html, "trust")
    opening = (
        '<div class="strato__lastre sez-plate sez-seq home-trust__grid integrita__tavola" data-trust="faq" '
        'data-verb="depth">'
    )
    assert block.count(opening) == 1 and block.count("sez-plate") == 1, "one plate, not four cards"
    tablet = block.split(opening, 1)[1]
    fields = re.findall(r'<article class="strato__lastra integrita__lastra" data-faq="([a-z_]+)"', tablet)
    assert fields == list(content.TRUST_FAQ_KEYS)
    plinth = tablet.split("</article>")[-1]
    assert re.search(r'<p class="integrita__azione"><a class="btn btn--secondary" href="/fr/faq/">', plinth)
    assert plinth.index('class="integrita__azione"') < plinth.index("</div>"), "the plinth is the tablet's own"
    sheet = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    # round 2 (QA_ROUND2 M2, SECTION_SYSTEM_V2 §5.3 INP; V5.20 strict rule): the bond names its fields, so the rule is
    # filed under their class and never tried against every element of the page on the first input's restyle — the
    # same four fields, the same 5 | 7 over 7 | 5
    spans = re.findall(r"\.integrita__tavola > \.integrita__lastra:is\([^{]*\) \{ grid-column: span (\d+); \}", sheet)
    assert spans == ["5", "7"], "5 | 7 over 7 | 5: the joints never line up"


def test_the_closed_gate_s_families_stand_on_the_index_s_tiles(page, seeded):
    """m1: with gate G3 closed the five neutral families are the index's own rows across the band — each its tile (the
    registry's glyph of the pathways it gathers, decorative) beside its word; nothing to select, nothing to open."""
    assert len(content.PATHWAY_FAMILY_KEYS) == len(content.PATHWAY_FAMILIES)
    _response, html = page("/fr/")
    block = html.split('data-section="pathways"', 1)[1].split("</section>", 1)[0]
    glyphs = re.findall(
        r'<span class="sez-tile home-families__tessera" aria-hidden="true"><svg class="icon"[^>]*>'
        r'<use href="[^"#]*#icon-([a-z-]+)"',
        block,
    )
    assert glyphs == [icons.PATHWAY[key] for key in content.PATHWAY_FAMILY_KEYS]
    assert "<a " not in block.split('class="indice__lista home-families')[1].split("</ul>", 1)[0], "nothing to open"


def test_the_stage_says_its_way_in_the_page_s_language_and_its_texts_in_their_own(page, seeded, phase3_open):
    """m4 (language of parts) and M2 b: on the Arabic page the prescribed description is its own French run (lang on the
    <p>), the way to the sheet is in the page's language — never inside a French box; the title's text stays the
    locked title, in the span its entrance inks."""
    from pathways import services as pathway_services

    _response, html = page("/ar/")
    block = html.split('data-section="pathways"', 1)[1].split("data-section=", 1)[0]
    assert '<div class="indice__corpo" lang=' not in block
    # the way to the sheet is said in the page's language — never the French it would fall back to (round 2,
    # QA_ROUND2: «Consulter la page du parcours» is in the ar catalogue; V5.20 strict rule, a stronger invariant than
    # round 1's «the French fallback, tagged»)
    from django.utils import translation

    with translation.override("ar"):
        said = translation.gettext("Consulter la page du parcours")
    assert said != "Consulter la page du parcours"
    links = re.findall(r'aria-describedby="parcours-[a-z-]+-title"([^>]*)>([^<]+)</a>', block)
    assert links and all(attrs == "" and text == said for attrs, text in links), links
    for entry in pathway_services.index_entries():
        anchor = f"parcours-{entry.key.replace('_', '-')}"
        panel = block.split(f'<section class="indice__pannello" id="{anchor}"', 1)[1].split("</section>", 1)[0]
        assert re.search(r'<p class="parcours__descrizione" lang="fr">', panel), entry.key
        heading = re.search(r'<h3 class="indice__titolo"[^>]*>(.*?)</h3>', panel).group(1)
        assert heading == f'<span class="indice__parola" data-verb="ink">{escaped(entry.title)}</span>', entry.key


def test_the_pilot_keeps_its_two_shores_on_one_line(page, seeded, phase3_open):
    """m5: «VÉNÉTIE–MAROC» never breaks after its dash — a render-time span (emphasis-free in pages.css), the heading's
    text the locked title itself."""
    title = locked_content.text("p3.pilot.title", "fr")
    _response, html = page("/fr/")
    block = _block(html, "pilot")
    heading = re.search(r'<h2 class="pilota__titolo" id="home-pilot-title">(.*?)</h2>', block).group(1)
    assert heading == escaped(title).replace("VÉNÉTIE–MAROC", '<span class="em-keyword">VÉNÉTIE–MAROC</span>')
    sheet = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    assert re.search(r"\.pilota__titolo \.em-keyword \{[^}]*white-space: nowrap;", sheet)


def test_the_reserved_key_stands_beside_its_button_in_the_identity_s_gold(page, seeded, phase3_open):
    """M1 d, m10: the seat beside «CONNEXION», where the eye is when the key turns; the key alone in the identity's
    gold, by a rule that wins over the night seat's ink (QA_ROUND1: the page rule lost on specificity)."""
    _response, html = page("/fr/")
    block = _block(html, "reserved")
    text, porta = block.split('<div class="home-reserved__porta">', 1)
    assert 'class="home-reserved__title"' in text and "sigillo" not in text
    assert porta.index('data-mark="ile-accesso"') < porta.index('class="btn btn--secondary home-reserved__button"')
    sheet = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    assert re.search(
        r"\.page-home \.home-reserved \.sigillo\.home-reserved__sigillo \.sg-g--key \{\s*color: var\(--identity-key\);",
        sheet,
    )


def test_the_ecosystem_photograph_rises_in_its_arch_and_its_doorway_is_drawn(page, seeded, phase3_open):
    """M1 e: the photograph rises in the arch (the verb «mask» on the frame's own wrapper); the sill and the arch's
    outline are one decorative drawing, each line drawn once (the verb «stroke»). V5.24 §2 (FINAL_DELIVERY_V2.md
    §3.2 D6): the frame carries no credit any more, so there is none to be masked — asserted absent."""
    _response, html = page("/fr/")
    block = _block(html, "ecosystem")
    frame = block.split('<div class="casa-arco" data-verb="mask">', 1)[1].split("</figure>", 1)[0]
    assert 'data-slot="home.ecosystem"' in frame and "<figcaption" not in frame
    drawing = re.search(r'<svg class="casa-arco__disegno"[^>]*>(.*?)</svg>', block)
    assert drawing and 'aria-hidden="true"' in drawing.group(0)
    # final fix round (QA_ROUND3 m1; V5.20 strict rule — SECTION_SYSTEM_V2 §3.1 S7 «the arch outline draws», §5.1 LINE
    # DRAW: one line, never segments): a stretched non-scaling stroke's dash is laid in DEVICE pixels, so round 2's
    # pathLength (0.1 and 0.125, a dash longer than the line at 1×) left a second dash on any screen of a higher pixel
    # ratio. Stronger: the two visible lines carry no dash and no verb at all; each is drawn through its own mask, whose
    # path is the line's own, in user space, carrying the verb with one dash a hair longer than itself
    # (_assert_drawn_through_masks); the browser half checks the PAINTED lines at 1×, 2× and 3×
    lines = _assert_drawn_through_masks(drawing.group(1))
    assert [(line["mask"], line["d"]) for line in lines] == [
        ("casa-arco-soglia", "M0 100H100"),
        ("casa-arco-profilo", "M0 100V41.5A50 41.5 0 0 1 100 41.5V100"),
    ], lines
    assert 'class="casa-arco__profilo"' in lines[1]["tag"] and 'class="casa-arco__profilo"' in lines[1]["mask_path"], (
        "the outline's per-width CSS path shapes the line and its mask alike"
    )
    sheet = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    # the aperture opens from the arch's foot: never inset at its sides or its foot, so the credit is never held
    assert re.search(r"--reveal-from: inset\(\d+% 0 0 0 round", sheet)


def test_the_round_1_rules_hold_the_reading_edge_and_the_arabic_page():
    """M1 c, M2 a–c, M1 b: «la protezione» hangs from the reading edge on the home, never centred; the route's
    origin seal is the body's 72 × 88 from 64 rem; on the Arabic page the route's French labels and the stage's French
    texts each start on their own edge, and the folio is never tracked nor set in a Latin monospace."""
    sheet = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    code = re.sub(r"/\*.*?\*/", "", sheet, flags=re.S)
    assert not re.search(r"protezione[^{]*\{[^}]*margin-inline: auto", code), "never centred off the reading edge"
    seal = r"\.home-orientation \.linea-v2 \.sigillo \{\s*--sg-w: 72px;\s*--sg-h: 88px;\s*--sg-m: 40px;"
    labels = r'\[dir="rtl"\] \.home-orientation \.linea-v2 li > p\[lang\] \{[^}]*text-align: start;'
    for rule in (seal, labels):
        assert re.search(rule, sheet), rule
    assert re.search(r"grid-template-columns: fit-content\(var\(--measure-lead\)\);", sheet)
    assert re.search(r"\.colofone__label:lang\(ar\) \{\s*font-family: var\(--f-sans\);\s*letter-spacing: 0;", sheet)


# ------------------------------------------------------------------------------------------ final fix round (QA_ROUND3)

_SHAPE = re.compile(r"<(?:path|circle|line|polyline|polygon|rect|ellipse)\b[^>]*>")


def _attrs(tag: str) -> dict:
    return dict(re.findall(r'([a-zA-Z-]+)="([^"]*)"', tag))


def _assert_drawn_through_masks(svg: str) -> list[dict]:
    """Each visible line of a drawing carries no dash: it is drawn through its own mask (user space, alpha: only the
    mask's opacity counts, never a literal colour) whose one path is the line's own path, in the drawing's user space
    (no vector-effect), carrying the verb «stroke» with one dash a hair longer than itself (pathLength 0.9–1), wide
    enough to cover the line, in the text's ink. Returns the visible lines in order."""
    masks = {}
    for mask_id, mask_attrs, inner in re.findall(r'<mask id="([^"]+)"([^>]*)>(.*?)</mask>', svg, flags=re.S):
        attrs = _attrs(mask_attrs)
        assert attrs.get("maskUnits") == "userSpaceOnUse" and attrs.get("mask-type") == "alpha", (mask_id, attrs)
        shapes = _SHAPE.findall(inner)
        assert len(shapes) == 1, (mask_id, shapes)
        path = _attrs(shapes[0])
        assert path.get("data-verb") == "stroke" and 0.9 <= float(path["pathLength"]) <= 1, (mask_id, path)
        assert "vector-effect" not in path and path.get("stroke") == "currentColor", (mask_id, path)
        assert float(path["stroke-width"]) >= 4, (mask_id, "the mask covers its line", path)
        masks[mask_id] = (shapes[0], path)
    outside = re.sub(r"<mask\b.*?</mask>", "", svg, flags=re.S)
    lines = []
    for tag in _SHAPE.findall(outside):
        attrs = _attrs(tag)
        mask_id = re.fullmatch(r"url\(#([^)]+)\)", attrs.get("mask", ""))
        assert mask_id and mask_id.group(1) in masks, ("a drawn line is masked by its own mask", tag)
        mask_tag, mask_path = masks.pop(mask_id.group(1))
        assert "data-verb" not in attrs and "pathLength" not in attrs, ("no dash on the visible line", tag)
        assert attrs.get("vector-effect") == "non-scaling-stroke", ("the 1 px line", tag)
        assert attrs["d"] == mask_path["d"], ("the mask's path is the line's own", tag, mask_tag)
        lines.append({"mask": mask_id.group(1), "d": attrs["d"], "tag": tag, "mask_path": mask_tag})
    assert not masks, ("every mask draws one line", masks)
    return lines


def test_final_round_no_line_of_the_home_lays_its_dash_on_a_non_scaling_stroke(page, seeded, phase3_open):
    """QA_ROUND3 m1, the class of the defect: on every screen of a higher pixel ratio than 1, a dash on a stretched
    non-scaling stroke paints a second dash (the doorway's far leg first, the phone doors' lunettes as dashes). On the
    home, in both scripts, no shape carries both — the verb «stroke» and a non-scaling stroke; the phone doors'
    lunettes, like the doorway, are drawn through their own masks, one per door (unique ids, the door's rank)."""
    for lang in ("fr", "ar"):
        _response, html = page(f"/{lang}/")
        main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
        both = [tag for tag in _SHAPE.findall(main) if 'data-verb="stroke"' in tag and "non-scaling-stroke" in tag]
        assert both == [], (lang, both)
        doors = re.findall(r'<svg class="passaggio__arco"[^>]*>(.*?)</svg>', main, flags=re.S)
        assert len(doors) == 4, (lang, len(doors))
        ids = [_assert_drawn_through_masks(door)[0]["mask"] for door in doors]
        assert ids == [f"passaggio-arco-{rank}" for rank in range(1, 5)], (lang, ids)
        assert len(re.findall(r'<mask id="', main)) == len(set(re.findall(r'<mask id="([^"]+)"', main))) == 6, lang


def test_final_round_the_arabic_titles_stand_against_their_glyphs_and_the_connector_on_its_rule():
    """QA_ROUND3 M1 and m2 in the home's sheet (the browser half measures them at the eight review widths):
    * the Arabic index's French titles are each the row's remainder, left to right in their own isolate and set against
      their glyph or tile — the end of their own box (the RTL label exception, SECTION_SYSTEM_V2 §2 F);
    * the colophon's connector runs on its folio's 2 px rule: half the folio's 1rem line, less half its own pixel."""
    sheet = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    titles = re.search(
        r'\[dir="rtl"\] \.home-pathways \[lang\] \.indice__nome,\s*'
        r'\[dir="rtl"\] \.home-pathways \[lang\] \.indice__parola \{([^}]*)\}',
        sheet,
    )
    assert titles, "the Arabic titles' rule"
    body = " ".join(titles.group(1).split())
    assert body == "flex: 1; direction: ltr; unicode-bidi: isolate; text-align: end;", body
    assert re.search(r"\.campata__ponte \{\s*inset-block-start: calc\(0\.5rem - 0\.5px\);\s*\}", sheet)
    tokens = (ROOT / "static" / "css" / "v5" / "tokens.css").read_text(encoding="utf-8")
    assert re.search(r"--t-folio-lh: 1rem;", tokens), "the connector's .5rem is half the folio's line"


# ------------------------------------------------------------------- after the final review (v522-h-final-qa1)


def test_final_review_the_arabic_pilot_title_takes_its_seam_s_alignment_and_the_lead_never_ends_on_one_word():
    """F-M1, F-m2 and F-m1 in the home's sheet (the browser half measures F-M1 and F-m2 at the eight review widths in
    the four languages, test_home_browser_v522_h.py):
    * on the Arabic page the pilot's French title follows its seam as its lead and link do — its lines end on the
      reading edge below 64 rem (the RTL label exception of SECTION_SYSTEM_V2 §2 F, two display lines), centred on
      the seam's axis from 64 rem — with a selector above the page-wide French-run rule (0,3,1), which held it at its
      own left;
    * the pilot's lead never ends on one word (text-wrap: pretty; «واحد.» alone at 768 before);
    * gate closed, the two interim plates each stand at their own height (one statement beside three left about 150 px
      of empty plate)."""
    sheet = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    code = re.sub(r"/\*.*?\*/", "", sheet, flags=re.S)
    title = r'\[dir="rtl"\] \.page-home \.pilota__titolo\[lang\] \{\s*text-align: (end|center);\s*\}'
    assert [m.group(1) for m in re.finditer(title, code)] == ["end", "center"], "below 64 rem, then from 64 rem"
    wide = next(b for b in code.split("@media (min-width: 64rem) {")[1:] if "(40cqi - 4rem)" in b).split("\n}\n", 1)[0]
    assert re.search(title.replace("(end|center)", "center"), wide), "the centred title lives in the 64 rem block"
    assert not re.search(title.replace("(end|center)", "end"), wide)
    assert re.search(r"\.pilota__lead \{[^}]*text-wrap: pretty;", code)
    assert re.search(r"\.strato__lastre--2 \{\s*align-items: start;\s*\}", code)


def test_final_review_the_home_reads_the_input_s_modality_in_one_rule(page, seeded, phase3_open):
    """F-M2, lane H's share (§5.3; the first keyboard input): the home's own sheets read the input's modality
    (html[data-input], head.js) in ONE rule — the doors' arrows and arches and the promoter's photograph settling in its
    arch, no duration left to run from the keyboard — each subject filed under a class (never a tag, an :is() or a
    universal subject, which the flip would try against every element). Measured, the home's own rules restyle no
    element at the first key (QA/v522/h/NOTES.md §14); the rest of the flip is the library's and main.css's."""
    rules = []
    for path in (
        ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css",
        ROOT / "apps" / "pages" / "static" / "pages" / "css" / "hero.css",
        ROOT / "static" / "css" / "v5" / "_casa.css",
    ):
        code = re.sub(r"/\*.*?\*/", "", path.read_text(encoding="utf-8"), flags=re.S)
        rules += [
            (path.name, m.group(1), m.group(2)) for m in re.finditer(r"([^{}]*data-input[^{}]*)\{([^}]*)\}", code)
        ]
    assert len(rules) == 1, rules
    name, selector, body = rules[0]
    subjects = [" ".join(part.split()) for part in selector.split(",")]
    assert name == "pages.css" and subjects == [
        'html[data-input="key"] .passaggio__freccia',
        'html[data-input="key"] .passaggio__arco',
        'html[data-input="key"] .campata__media .foto__img',
    ], subjects
    assert " ".join(body.split()) == "transition-duration: 0s;", body
    _response, html = page("/fr/")
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    assert main.count('class="icon passaggio__freccia') == 4 and main.count('<svg class="passaggio__arco"') == 4
    assert re.search(r'<div class="[^"]*campata__media[^"]*"[^>]*>.*?class="foto__img', main, flags=re.S)
