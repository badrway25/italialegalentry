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
  own heights (F-m1), and the home's sheets read the input's modality in one rule (F-M2, lane H's share);
* V5.24 (lane HOME, label v524-home; BACKGROUND_MATERIAL_V2 §3.1–§3.3, §5.1; TYPOGRAPHY_V2 §4.2, §6; FINAL_DELIVERY_V2
  R3, §3.4; V5.20 strict rule, each change cited where it stands): the index on stone and «la protezione» on «pietra» —
  stone and pietra ONE kind for the adjacency rule, which the resolver now flips by kind; the orientation's sfumatura
  and the pilot's raccordo follow the resolved grounds; the material partial imported by the home's sheet before «la
  casa»; the colophon's label is the label role by name (its Arabic the role's rule, no page rule); the raccordo's gold
  is the pilot's thread continued (the same object, named in «la casa», never a fourth use).
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


def _bands(html: str) -> list[dict]:
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    out = []
    for tag in re.findall(r"<section class=\"sez [^>]*>", main):
        attrs = dict(re.findall(r'([a-z-]+)="([^"]*)"', tag))
        out.append(attrs)
    return out


def _sections(html: str) -> list[dict]:
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B): a chapter may draw a second band of its own (the trust partial's FAQ preview, `data-sub`); the
    # chapters are the bands that carry their `data-section`, and _bands keeps every band for the grounds' rule
    return [band for band in _bands(html) if "data-section" in band]


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
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B): every band — the chapters and the FAQ preview, the one sub-band — is held to the V2 rules, and the
    # grounds' rule reads every band (stronger: the sub-band's ground counts)
    bands = _bands(html)
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 1): the FAQ preview is a
    # chapter of its own — it carries its `data-section` (and keeps its `data-sub` name), so NO band is left without
    # one: every band of the home is a chapter, held to the V2 rules and read by the grounds' rule
    assert [b for b in bands if "data-section" not in b] == []
    assert [b["data-section"] for b in bands if b.get("data-sub")] == (["faq"] if state == "open" else [])
    for s in bands:
        assert s["data-ground"] in {"paper", "stone", "pietra", "brand", "night", "photo"}, s
        assert s["data-rhythm"] in {"strip", "band", "moment"}, s
        label = s["aria-labelledby"]
        assert re.search(rf'<h2 [^>]*id="{label}"', html), (s.get("data-section", s.get("data-sub")), "its head")
    grounds = ["paper"] + [s["data-ground"] for s in bands]  # the hero's wall first
    # V5.24 (BACKGROUND_MATERIAL_V2 §3.3; FINAL_DELIVERY_V2 R3, §3.4): stone and pietra are ONE kind — the same colour —
    # so «two grounds of one kind never touch» now reads by kind: pietra never touches stone, stone never pietra
    kind = {"pietra": "stone"}.get
    for before, after in zip(grounds, grounds[1:]):
        assert kind(before, before) != kind(after, after), grounds
    # one brand wash a page, and one moment, placed second or third below the header on desktop (§1 rule 5)
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§10, lane B «il viaggio»): the orientation's wash became the deep ink band — no wash is left under the hero
    assert grounds.count("brand") == 0
    if state == "open":
        assert [s["data-section"] for s in sections if s["data-rhythm"] == "moment"] == ["pilot"]


def test_the_grounds_hold_when_the_back_office_reorders_or_adds_a_section(page, seeded, phase3_open, article_factory):
    """The news between «la protezione» (stone) and the promoter (paper) would set two papers side by side: the promoter
    takes the stone; an editor who moves the pathways right under the hero gives them the stone under the paper wall."""
    article_factory("Programme du Forum publié")
    _response, html = page("/fr/")
    by_key = {s["data-section"]: s["data-ground"] for s in _sections(html)}
    # V5.24 (FINAL_DELIVERY_V2 §3.4 S3, S6): the index on stone, «la protezione» on pietra (one kind with stone: the
    # promoter after the news still takes the stone — a stone two sections after the pietra, never touching it)
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B): the FAQ preview, the trust partial's second band, stands on the stone after the clarity's paper, so
    # the warning that follows it takes the paper (its ochre plate stands on it) and the news and promoter alternate
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (points 1 and 4): the narrative —
    # clarity (paper), the ecosystem (stone), the FAQ preview (paper), the news (stone), then the warning LAST: its
    # dark plate stands on the paper — the two light kinds alternating all the way down
    assert [b["data-ground"] for b in _bands(html) if b.get("data-sub") == "faq-preview"] == ["paper"]
    assert (by_key["trust"], by_key["pathways"], by_key["ecosystem"], by_key["news"], by_key["antifraud"]) == (
        "paper",
        "stone",
        "stone",
        "stone",
        "paper",
    ), by_key
    assert [s["data-section"] for s in _sections(html)][-1] == "antifraud"
    HomeSection.objects.filter(key__in=[SectionKey.ENTRANCES, SectionKey.ORIENTATION]).update(is_enabled=False)
    _response, html = page("/fr/")
    assert _sections(html)[0]["data-section"] == "pathways"
    assert _sections(html)[0]["data-ground"] == "stone", "never paper under the hero's paper wall"


def test_the_grounds_resolver_flips_only_the_two_light_grounds():
    """V5.24 (BACKGROUND_MATERIAL_V2 §3.3; FINAL_DELIVERY_V2 §3.4): the pathways are stone now — under the hero's paper
    wall they stay stone; pietra after a stone band (the back office's reorder) takes the paper, as a stone after a
    stone did; a paper after a pietra needs no flip. The seams follow the resolved grounds: the orientation's foot
    dissolves into the next light ground (its kind), the pilot's seam begins above the night only after a light band."""

    def resolve(*keys):
        views = [services.SectionView(key=key, template="", anchor="", data={}) for key in keys]
        services._grounds(views)
        return views

    views = resolve(SectionKey.HERO, SectionKey.PATHWAYS, SectionKey.NEWS, SectionKey.PILOT, SectionKey.RESERVED)
    assert [v.ground for v in views[1:]] == ["stone", "paper", "night", "night"]
    views = resolve(SectionKey.HERO, SectionKey.ENTRANCES, SectionKey.ANTIFRAUD, SectionKey.PATHWAYS, SectionKey.NEWS)
    assert [v.ground for v in views[1:]] == ["stone", "paper", "stone", "paper"], "pietra after stone takes the paper"
    views = resolve(SectionKey.HERO, SectionKey.ENTRANCES, SectionKey.NEWS, SectionKey.ANTIFRAUD, SectionKey.ECOSYSTEM)
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 4: the ochre block on the
    # dressed stone is rejected): the warning is a dark plate on a LIGHT ground of the two kinds, no longer «pietra» —
    # after the news' paper it takes the stone, and the paper after it needs no flip; the resolver still flips only
    # the two light grounds, and no home section asks for pietra
    assert [v.ground for v in views[1:]] == ["stone", "paper", "stone", "paper"], "paper after paper: the stone"
    assert "pietra" not in services.SECTION_GROUNDS.values()
    assert services.LIGHT_KIND == {"paper": "paper", "stone": "stone", "pietra": "stone"}
    # the seams
    views = resolve(SectionKey.HERO, SectionKey.ORIENTATION, SectionKey.PATHWAYS, SectionKey.PILOT, SectionKey.TRUST)
    assert [v.sfuma for v in views] == ["", "stone", "", "", ""], "the wash dissolves into the index band's stone"
    assert views[3].data == {"raccordo": True}, "the pilot's seam begins above the night after a light band"
    views = resolve(SectionKey.HERO, SectionKey.ORIENTATION, SectionKey.PILOT, SectionKey.ANTIFRAUD, SectionKey.NEWS)
    assert [v.sfuma for v in views] == ["", "", "", "", ""], "no sfumatura into the night"
    assert views[2].data == {"raccordo": False}, "no raccordo out of the wash"
    views = resolve(SectionKey.HERO, SectionKey.ORIENTATION, SectionKey.ANTIFRAUD, SectionKey.PILOT)
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 4): the warning stands on a
    # light ground of the two kinds (paper under the orientation's night), no longer on pietra — the seam still
    # follows the resolved ground, and the pilot's still begins after a light band
    assert views[1].sfuma == "paper" and views[3].data == {"raccordo": True}, "the seam follows the resolved ground"
    views = resolve(SectionKey.HERO, SectionKey.ORIENTATION, SectionKey.NEWS, SectionKey.PILOT)
    assert views[1].sfuma == "paper"


# ---------------------------------------------------------------------------------------------- H0, S2


@pytest.mark.parametrize("state", ["closed", "open"])
def test_no_line_leaves_the_hero_and_the_orientation_keeps_its_origin_seal(request, page, seeded, state):
    """V5.30 Fast Visual Variety Correction §5 (a line with no semantic value goes; §3: the band under the hero's
    arch speaks
    a different language). V5.20 strict rule: this decision replaces «the hero line runs on into the route». Nothing is
    drawn between the statement and the band; the statement, the band's head and the route's origin, the T1 seal of
    orientation, all stand."""
    if state == "open":
        request.getfixturevalue("phase3_open")
    _response, html = page("/fr/")
    hero = html.split('data-section="hero"', 1)[1].split("</section>", 1)[0]
    assert "he__soglia" not in hero and 'data-sec="soglia"' not in hero
    assert '<div class="he__statement">' in hero
    block = _block(html, "orientation")
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§10–§11, lane B «il viaggio»): the head, then the journey of four moments; the first moment is its semantic
    # glyph (the compass) and its keyword, as the three after it are theirs — no seal, no numeral
    capo = block.split('<div class="viaggio__capo">', 1)[1].split('<div class="viaggio__corpo"', 1)[0]
    assert "orienta__soglia" not in capo and 'id="home-orientation-title"' in capo
    route = block.split('<div class="viaggio__corpo"', 1)[1]
    first_moment = route.split('<li class="viaggio__tappa">', 2)[1]
    assert "sigillo" not in route and "sez-tile" not in route and "linea__num" not in route
    assert '<span class="viaggio__glifo" aria-hidden="true">' in first_moment and "#icon-compass" in first_moment
    assert 'class="viaggio__nome"' in first_moment and 'class="viaggio__parole"' in first_moment


def test_the_orientation_route_is_the_locked_sentence_cut_and_said_once(page, seeded, phase3_open):
    from pathways.services import how_it_works

    cut = how_it_works("fr")
    data = services.build_orientation(services.BuildContext(request=None, lang="fr", phase3=True))
    assert [s["label"] for s in data["stations"]] == list(cut.steps)
    # FINAL MICRO-PASS §5 A2 (V5.20 strict rule): a station carries no glyph — its marker is its place in the sequence
    assert all("glyph" not in s for s in data["stations"])
    assert data["whole"] == locked_content.text("p3.persons.how_it_works", "fr")
    _response, html = page("/fr/")
    block = _block(html, "orientation")
    assert block.count(escaped(cut.caveat)) == 2, "the caveat: drawn once at the route's end, said once in the whole"
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B): the call is the action panel's primary button, its arrow mirrored on the Arabic page
    assert 'class="btn btn--primary viaggio__cta" href="/fr/orientation/" data-azione>' in block, "the call"


def test_the_orientation_route_in_another_language_carries_the_french_it_is_cut_from(page, seeded, phase3_open):
    # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): p3.persons.how_it_works is
    # compositional (C-UI) — on /ar/ the route carries its provisional Arabic rendering, said once whole and cut from
    # it, in the page's language: no French run left in the block
    from cms import locked_renderings

    _response, html = page("/ar/")
    block = _block(html, "orientation")
    whole = re.search(r'<p class="visually-hidden">(.*?)</p>', block, flags=re.S)
    rendering = locked_renderings.rendering("p3.persons.how_it_works")
    assert whole and whole.group(1) == rendering, "the whole sentence, once"
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B «il viaggio»): the four stations drawn in the moments, hidden from a reader that heard the whole
    assert block.count('<span class="viaggio__parole" aria-hidden="true">') == 4
    assert '<p class="orienta__avvertenza" aria-hidden="true">' in block
    assert 'lang="fr"' not in block


def test_the_orientation_gate_closed_ends_on_the_editorial_note(page, seeded):
    _response, html = page("/fr/")
    block = _block(html, "orientation")
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B): the editorial note is the action panel's reassurance, its button the one call
    panel = block.split('<div class="viaggio__azione">', 1)[1]
    assert '<div class="viaggio__garanzia"><span class="viaggio__info" aria-hidden="true">' in panel
    assert '<p class="orienta__avvertenza">' in panel.split('class="viaggio__garanzia"', 1)[1]
    assert "pré-évaluation à caractère informatif" in panel.split('class="viaggio__garanzia"', 1)[1]
    assert block.count("data-azione><span>Commencer le questionnaire d’orientation</span>") == 1


# ---------------------------------------------------------------------------------------------- S3


def test_the_pathways_stage_links_a_published_sheet_and_only_that(page, seeded, phase3_open):
    from pathways import services as pathway_services

    _response, html = page("/fr/")
    block = _block(html, "pathways")
    for entry in pathway_services.index_entries():
        anchor = f"parcours-{entry.key.replace('_', '-')}"
        panel = block.split(f'<section class="esplora__pannello" id="{anchor}"', 1)[1].split("</section>", 1)[0]
        # round 2 (QA_ROUND2, institutional quality on it/en/ar; V5.20 strict rule — SECTION_SYSTEM_V2 §1 rule 6,
        # the language of parts): the way to the sheet is the product's own words for it, the orientation result's
        # «Consulter la page du parcours», a msgid the it/en/ar catalogues already hold (never a fallback)
        if entry.url:
            assert f'href="{entry.url}" aria-describedby="{anchor}-title">Consulter la page du parcours</a>' in panel
        else:
            assert "Consulter la page du parcours" not in panel, entry.key
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B «l'esploratore»): the space is the rail's closing card, named once
    assert len(re.findall(r'class="[^"]*\bhome-pathways__more\b', block)) == 1, "the space, named once"
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§14, lane B «l'esploratore»): the explorer is the home's own tabs (home.js), never the library's index module
    assert 'data-tabs="parcours"' in block and 'data-sec-js="indice"' not in block


# ---------------------------------------------------------------------------------------------- S4


def test_the_pilot_lead_says_what_the_panel_shows(page, seeded, phase3_open):
    assert services.str_source(content.SECTION_DEFAULTS_BY_KEY[SectionKey.PILOT].intro) == (
        "Le même geste, sur le cèdre et sur le marbre : deux savoir-faire, deux rives, un même projet."
    )
    _response, html = page("/fr/")
    block = _block(html, "pilot")
    assert "Le même geste, sur le cèdre et sur le marbre" in block
    assert OLD_PILOT_LEAD not in html and "étape par étape" not in block
    # the panel: two panels of lane M's re-crops, developing; one link; nothing ranked. V5.30 Fast Visual Variety
    # Correction §5 (V5.20 strict rule): no gold thread nor seam is drawn between them, the two gestures carry it
    assert block.count('data-slot="home.pilot.') == 2 and block.count('data-grade="bw-scroll"') == 2
    assert "2x3-" in block, "the full-height 2:3 panels (variant «pannello»)"
    assert "pilota__filo" not in block and "panorama__cucitura" not in block


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
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 1): the questions are the FAQ
    # preview's own section now (data-section="faq") — the same invariant, read in its block
    block = _block(html, "faq")
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§20, lane B «le domande»): the featured question's title and each folded question's way open its own entry
    hrefs = re.findall(r'<a class="(?:domanda__link|link-arrow)" href="(/fr/faq/#[^"]+)"', block)
    assert hrefs == [f"/fr/faq/#{key}" for key in content.TRUST_FAQ_KEYS]
    faq = client.get("/fr/faq/").content.decode("utf-8")
    for key in content.TRUST_FAQ_KEYS:
        assert f'id="{key}"' in faq, (key, "the FAQ keeps the permalink the plate opens")
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§19–§20, lane B): the masonry frame under the answers left with the plate — the clarity and the questions stand
    # on their surfaces; asserted absent, so the veiled photograph cannot silently return
    assert "integrita__fondo" not in block and 'data-slot="home.integrity.stone"' not in block
    assert "data-parallax" not in block


def test_the_warning_closes_the_band_with_the_one_plate_of_every_page(page, seeded, phase3_open):
    _response, html = page("/fr/")
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (points 1 and 4): the warning is
    # the page's LAST section before the footer (it followed the trust chapter) — stronger: last in the page's order
    # and last band of <main>
    assert section_order(html)[-1] == "antifraud"
    assert _bands(html)[-1]["data-section"] == "antifraud"
    block = _block(html, "antifraud")
    # V5.29 (owner: «protezione__campo too dominant … compact»; stream SYS; V5.20: the same invariant — one plate, the
    # band's — on a plain plate: the compact band carries no raised shadow)
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§22, lane B «l'allerta»): the home draws its own warning band — one ochre plate, the band's
    assert block.count('<div class="allerta" data-callout="antifraud">') == 1
    assert '<aside class="protezione' not in block
    assert 'aria-labelledby="protezione-title-home"' in html and 'id="protezione-title-home"' in block
    assert text_of("p3.antifraud.title") in block


# ---------------------------------------------------------------------------------------------- S7, S8


def test_the_promoter_stands_beside_the_working_table_under_the_arch(page, seeded, phase3_open):
    """S7: the promoter after the working table. RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD
    directive of 10 Nov 2026 (§24–§25; lane A): the
    section is an image-led media split — lane M's 4:3 frame of the working table, the head beside it — then the
    promoter's dark band: AGAMI's own logo and seal (lazy: the home's one LCP is the door), the Italian name, three
    verified facts that are phrases of the prescribed answer (aria-hidden), the answer with its two ink keywords, ONE
    call. The same invariants on the content; stronger on the composition: no arch, no campata, no «intesa», and the
    marks never eager."""
    _response, html = page("/fr/")
    block = _block(html, "ecosystem")
    assert '<div class="container eco-split">' in block and "campata" not in block and "casa-arco" not in block
    assert "intesa" not in block, "no Italy + Morocco primitive under the band (its own fields are aria-hidden)"
    assert '<div class="agami-banda__campi" aria-hidden="true">' in block
    assert 'data-slot="home.ecosystem"' in block and "4x3-" in block, "lane M's 4:3 re-crop in its plain frame"
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 3): ONE AGAMI mark — the
    # official lockup, lazy, never eager; the round seal left the band (asserted absent)
    assert re.findall(r'data-mark="([a-z.]+)"', block) == ["agami.insegna"]
    for key in ("agami.insegna",):
        mark = re.search(rf'<picture class="[^"]*" data-mark="{key}">.*?</picture>', block, flags=re.S).group(0)
        assert 'loading="lazy"' in mark and "fetchpriority" not in mark, key
    assert '<span class="fronte__name" lang="it" dir="ltr">AGAMI</span>' in block
    for keyword in ("depuis 2011", "Italie–Maroc"):
        assert f'<span class="em-keyword">{keyword}</span>' in block, keyword
    answer = next(e for e in locked_content.get("p3.faq.items", "fr")[0] if e["key"] == "faq_who")["answer"]
    facts = re.search(r'<ul class="agami-fatti[^"]*" role="list" aria-hidden="true">(.*?)</ul>', block, flags=re.S)
    labels = re.findall(r"<span>([^<]+)</span>", facts.group(1))
    assert labels == ["Association de juristes", "Depuis 2011", "Dialogue juridique Italie–Maroc"]
    for label in labels:
        assert label.lower() in answer.lower(), ("a fact is a phrase of the prescribed answer", label)
    assert block.count('class="home-cta home-cta--night"') == 1


# ---------------------------------------------------------------------------------------------- sheets, budgets


def _gz(path: Path) -> int:
    return len(gzip.compress(path.read_bytes(), 9))


def test_the_home_sheets_are_page_only_and_under_their_ceilings():
    """SECTION_SYSTEM_V2 §7.1: pages.css ≤ 12 288, hero.css ≤ 11 264 (H0 only), main.css never above 32 105 B gzip -9;
    the home's partial «la casa» and the library's pattern partials are imported by the home's sheet, never by
    main.css."""
    # V5.30 §7 (stream A; V5.20, re-recorded at the measure with test_frontispiece_v515_c.py's SHEETS — NOTES
    # docs/design-v5/QA/v530/art/NOTES.md §6): the Italy + Morocco primitive on the cooperation moment, the arch's
    # rules paid
    assert _gz(DIST / "pages" / "css" / "pages.css") <= 11_626
    assert _gz(DIST / "pages" / "css" / "hero.css") <= 10_849
    assert _gz(DIST / "main.css") <= 32_105
    source = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 2): the reserved closing row —
    # the home's last seal — left the home's composition (pages.services.HOME_OMITS), so the home's sheet no longer
    # imports the seat's sheet it draws nothing with; the invariant is stated the other way round, as strongly
    assert '@import url("../../css/v5/_sigillo.css")' not in source, "the home draws no seal: no seat's rules"
    for partial in (
        "_sezioni",
        "_sec-passaggio",
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026: the promoter's
        # «campata» left the home
        # (lane A: the media split and the promoter's band are v5/_home-a.css's), so the home imports the lane sheet it
        # draws instead — after «la casa», asserted below
        "_materia",
        "_casa",
        "_home-a",
    ):
        assert f'@import url("../../css/v5/{partial}.css");' in source, partial
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B): the home imports only the library parts it draws — the route, the index's tabs and the plates left
    # with the orientation, the pathways and the trust they drew, so their partials are asserted NOT imported
    for gone in ("_linea-v2", "_sec-indice-base", "_sec-lastre"):
        assert f'css/v5/{gone}.css")' not in source, gone
    # V5.24 (FINAL_DELIVERY_V2 R3, §3.4): the material partial after the shell and before «la casa», which places it
    imports = re.findall(r'@import url\("\.\./\.\./css/v5/(_[a-z0-9-]+)\.css"\);', source)
    assert imports.index("_sezioni") < imports.index("_materia") < imports.index("_casa") < imports.index("_home-a")
    assert "_sec-campata" not in imports, "the home draws no campata: a page carries only what it draws"
    lane = (ROOT / "static" / "css" / "v5" / "_home-a.css").read_text(encoding="utf-8")
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(", re.sub(r"/\*.*?\*/", "", lane, flags=re.S)), "tokens only"
    main = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
    assert "_casa" not in main and "_sezioni" not in main and "_materia" not in main
    casa = (ROOT / "static" / "css" / "v5" / "_casa.css").read_text(encoding="utf-8")
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|\brgba?\(", re.sub(r"/\*.*?\*/", "", casa, flags=re.S)), "tokens only"


def test_the_home_moves_nothing_of_its_own_and_spends_its_gold_on_the_key():
    """The home's sheets animate nothing (every entrance is a verb of v5/_reveal.css); gold in the home's sheet is the
    key's identity (§4.5) — nothing else. V5.30 Fast Visual Variety Correction §5 (V5.20 strict rule; the invariant is
    stronger): the pilot's thread and its raccordo were the sheet's other gold and left with their drawings, so «la
    casa»
    names no gold at all."""
    sheet = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    code = re.sub(r"/\*.*?\*/", "", sheet, flags=re.S)
    assert "animation" not in sheet and "@keyframes" not in code
    gold = re.findall(r"var\((--(?:identity-light|identity-key|p-oro-300|he-gold[a-z-]*))\)", code)
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 2): the key in the reserved
    # row was the sheet's one gold and left with the row — the home's sheet names no gold at all (stronger)
    assert gold == [], gold
    casa = re.sub(
        r"/\*.*?\*/", "", (ROOT / "static" / "css" / "v5" / "_casa.css").read_text(encoding="utf-8"), flags=re.S
    )
    assert "animation" not in casa and "transition" not in casa, "nothing in «la casa» moves"
    gold_rules = [
        sel.strip()
        for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", casa)
        if re.search(r"identity-(light|key)|he-gold|p-oro", body)
    ]
    assert gold_rules == [], gold_rules


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
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§10, lane B «il viaggio»): the line no longer runs on from the hero (V5.30 §5 already drew none) — the band is
    # the deep ink journey; no portico, no needle, and its only drawings are its semantic glyphs, all decorative
    assert "home-orientation--soglia" not in html and "sez--linea" not in html
    block = _block(html, "orientation")
    assert "orienta-ago" not in block and "orienta__portico" not in block
    assert all('aria-hidden="true"' in svg for svg in re.findall(r"<svg\b[^>]*>", block))


def test_the_trust_answers_are_one_tablet_set_in_the_wall_with_its_plinth(page, seeded, phase3_open):
    """M1 (trust): «four equal white cards» become ONE raised plate — four fields in the masonry's running bond, the way
    to every question its plinth inside it; each field still opens its own FAQ entry; the plate settles once (depth)."""
    _response, html = page("/fr/")
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 1): read in the FAQ preview's
    # own section
    block = _block(html, "faq")
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§20, lane B «le domande»): «four equal white cards» never return — the four answers are ONE preview: the first
    # question featured (its answer shown), the other three folded in one exclusive group of real <details>; the way
    # to every question is the band's own, in its head; no plate, no card grid
    opening = '<div class="domande__griglia" data-trust="faq">'
    assert block.count(opening) == 1 and "sez-plate" not in block and "strato__lastra" not in block
    grid = block.split(opening, 1)[1]
    fields = re.findall(r'<(?:article|details) class="domanda [^"]*"(?: name="home-faq")? data-faq="([a-z_]+)"', grid)
    assert fields == list(content.TRUST_FAQ_KEYS)
    assert grid.count('<article class="domanda domanda--prima"') == 1
    assert grid.count('<details class="domanda domanda--breve" name="home-faq"') == 3
    head = block.split('<div class="domande__capo">', 1)[1].split(opening, 1)[0]
    assert re.search(r'<a class="domande__tutte link-arrow" href="/fr/faq/">', head), "the way to every question"


def test_the_closed_gate_s_families_stand_on_the_index_s_tiles(page, seeded):
    """m1: with gate G3 closed the five neutral families are the index's own rows across the band — each its tile (the
    registry's glyph of the pathways it gathers, decorative) beside its word; nothing to select, nothing to open."""
    assert len(content.PATHWAY_FAMILY_KEYS) == len(content.PATHWAY_FAMILIES)
    _response, html = page("/fr/")
    block = html.split('data-section="pathways"', 1)[1].split("</section>", 1)[0]
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B «l'esploratore»): the families stand as still chips on the explorer's own tiles
    glyphs = re.findall(
        r'<span class="esplora__tessera" aria-hidden="true"><svg class="icon"[^>]*>'
        r'<use href="[^"#]*#icon-([a-z-]+)"',
        block,
    )
    assert glyphs == [icons.PATHWAY[key] for key in content.PATHWAY_FAMILY_KEYS]
    assert "<a " not in block.split('<ul class="home-families"')[1].split("</ul>", 1)[0], "nothing to open"


def test_the_stage_says_its_way_in_the_page_s_language_and_its_texts_in_their_own(page, seeded, phase3_open):
    """m4 (language of parts) and M2 b: the way to the sheet is in the page's language — never inside a French box; the
    title's text is the prescribed title in the span its entrance inks. V5.27 / R7′ (V5.20 strict rule, an approved
    decision — FINAL_DELIVERY_V2 §3.9, AR NOTES §4 «HOME»; stronger than «the French run, tagged»): on the Arabic page
    the title reads its provisional Arabic rendering and the description, quoted off its own page, stands in its
    hidden form — the Arabic pointer line, no `lang` of another language, no French word of the source."""
    from pathways import services as pathway_services

    _response, html = page("/ar/")
    block = html.split('data-section="pathways"', 1)[1].split("data-section=", 1)[0]
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B «l'esploratore»): the stage's body, never inside a French box
    assert '<div class="esplora__corpo" lang=' not in block and '<div class="indice__corpo" lang=' not in block
    # the way to the sheet is said in the page's language — never the French it would fall back to (round 2,
    # QA_ROUND2: «Consulter la page du parcours» is in the ar catalogue; V5.20 strict rule, a stronger invariant than
    # round 1's «the French fallback, tagged»)
    from django.utils import translation

    with translation.override("ar"):
        said = translation.gettext("Consulter la page du parcours")
    assert said != "Consulter la page du parcours"
    links = re.findall(r'aria-describedby="parcours-[a-z-]+-title"([^>]*)>([^<]+)</a>', block)
    assert links and all(attrs == "" and text == said for attrs, text in links), links
    from cms import locked_renderings

    locked_renderings.set_route_for_tests("pages:home")
    try:
        with translation.override("ar"):
            arabic = pathway_services.index_entries(lang="ar")
    finally:
        locked_renderings.set_route_for_tests(None)
    for french, entry in zip(pathway_services.index_entries(), arabic, strict=True):
        anchor = f"parcours-{entry.key.replace('_', '-')}"
        panel = block.split(f'<section class="esplora__pannello" id="{anchor}"', 1)[1].split("</section>", 1)[0]
        assert entry.description_hidden and not entry.description_lang and not entry.title_lang, entry.key
        assert f'<p class="parcours__descrizione">{escaped(entry.description)}</p>' in panel, entry.key
        assert escaped(french.description) not in panel and entry.title != french.title, entry.key
        # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
        # (lane B): the stage's heading carries no lang of another language; its text the prescribed title in its span
        heading = re.search(rf'<h3 class="esplora__titolo" id="{anchor}-title">(.*?)</h3>', panel).group(1)
        assert heading == f'<span class="indice__parola" data-verb="ink">{escaped(entry.title)}</span>', entry.key


def test_the_pilot_keeps_its_two_shores_on_one_line(page, seeded, phase3_open):
    """m5: «VÉNÉTIE–MAROC» never breaks after its dash — a render-time span (emphasis-free in pages.css), the heading's
    text the locked title itself."""
    title = locked_content.text("p3.pilot.title", "fr")
    _response, html = page("/fr/")
    block = _block(html, "pilot")
    heading = re.search(r'<h2 class="pilota__titolo" id="home-pilot-title">(.*?)</h2>', block).group(1)
    assert heading == escaped(title).replace("VÉNÉTIE–MAROC", '<span class="em-keyword">VÉNÉTIE–MAROC</span>')
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026: the pilot's rules are
    # lane A's sheet's
    sheet = (ROOT / "static" / "css" / "v5" / "_home-a.css").read_text(encoding="utf-8")
    assert re.search(r"\.pilota__titolo \.em-keyword \{[^}]*white-space: nowrap;", sheet)


def test_the_ecosystem_photograph_rises_in_its_arch_and_its_doorway_is_drawn(page, seeded, phase3_open):
    """M1 e asked the photograph to rise in the arch and its doorway to be drawn once; V5.30 made the frame plain.
    RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§24, lane A): the
    photograph leads a media split — it opens from its
    edge by the photo component's mask (v5/_reveal.css M2) and bleeds to the viewport's reading edge from 64 rem —, with
    no credit (V5.24 §2: asserted absent); the arch's mask, its sill and its outline stay asserted ABSENT from the
    markup
    and from the home's sheets, so the old doorway cannot silently return."""
    _response, html = page("/fr/")
    block = _block(html, "ecosystem")
    media = block.split('<div class="eco-split__media">', 1)
    assert len(media) == 2, "the media split's frame"
    frame = media[1].split("</figure>", 1)[0]
    assert 'data-slot="home.ecosystem"' in frame and 'data-reveal="mask"' in frame and "<figcaption" not in frame
    assert "casa-arco" not in block and "<mask" not in block, "no arch mask, no doorway drawn"
    sheet = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    lane = (ROOT / "static" / "css" / "v5" / "_home-a.css").read_text(encoding="utf-8")
    assert "casa-arco" not in sheet and "casa-arco" not in lane, "the doorway's rules left the home's sheets"
    assert re.search(r"\.eco-split__media \{\s*grid-column: 1 / span 7;\s*margin-inline-start: calc\(-1 \*", lane), (
        "the frame bleeds to the reading edge"
    )


def test_the_round_1_rules_hold_the_reading_edge_and_the_arabic_page():
    """M1 c, M2 a–c, M1 b: «la protezione» hangs from the reading edge on the home, never centred; the route's
    origin seal is one of its panel's 48 px tiles (V5.30 Fast Visual Variety Correction §7 HOME, §4; V5.20 strict
    rule: it
    was the body's 72 × 88 on the route's line); on the Arabic page the route's French labels and the stage's French
    texts each start on their own edge, and the folio is never tracked nor set in a Latin monospace."""
    sheet = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    code = re.sub(r"/\*.*?\*/", "", sheet, flags=re.S)
    assert not re.search(r"protezione[^{]*\{[^}]*margin-inline: auto", code), "never centred off the reading edge"
    # FINAL MICRO-PASS §5 A1/A2 (V5.20 strict rule): the route's origin seal left with its seat — no rule sizes it any
    # more; the Arabic page's French labels still start on their own edge
    assert "linea__segno" not in code and not re.search(r"\.home-orientation[^{]*\.sigillo", code)
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B «il viaggio»): the route left; the Arabic page's French words in the moments still start on their own
    # edge — the rule is the lane's sheet's, and the old route is asserted gone
    assert "linea-v2" not in code
    lane = (ROOT / "static" / "css" / "v5" / "_home-b.css").read_text(encoding="utf-8")
    labels = (
        r'\[dir="rtl"\] \.home-orientation :is\(\.viaggio__parole, \.viaggio__frase\)\[lang\] \{[^}]*text-align: start;'
    )
    assert re.search(labels, lane), labels
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B «l'esploratore»): the stage's French title and description still hang from one edge — the lane's rule
    assert re.search(
        r'\[dir="rtl"\] \.esplora__testo:has\(> \[lang\]\) \{\s*'
        r"grid-template-columns: fit-content\(var\(--measure-lead\)\);",
        lane,
    )
    # V5.24 (TYPOGRAPHY_V2 F-3 / F-4; FINAL_DELIVERY_V2 §3.4; V5.20 strict rule): the folio is the label role by name —
    # `t-label` on the colophon's labels, whose Arabic (the page's face, no tracking, no capitals) is the role's own
    # rule in v5/base.css; the page rule that said the same is gone (the invariant held by the system, not restated)
    colophon = (ROOT / "templates" / "pages" / "home" / "_ecosystem_colophon.html").read_text(encoding="utf-8")
    assert colophon.count('class="testa__label colofone__label t-label"') == 2, (
        "the promoter's and the partners' labels"
    )
    assert ".colofone__label:lang(ar)" not in sheet
    base = (ROOT / "static" / "css" / "v5" / "base.css").read_text(encoding="utf-8")
    assert re.search(
        r":is\([^)]*\.t-label[^)]*\):lang\(ar\)[^{]*\{[^}]*letter-spacing: 0;[^}]*text-transform: none;", base
    )
    assert re.search(r"\.t-label, \.eyebrow \{\s*font-family: var\(--f-sans\);", base)


# ------------------------------------------------------------------------------------------ final fix round (QA_ROUND3)

_SHAPE = re.compile(r"<(?:path|circle|line|polyline|polygon|rect|ellipse)\b[^>]*>")


def test_final_round_no_line_of_the_home_lays_its_dash_on_a_non_scaling_stroke(page, seeded, phase3_open):
    """QA_ROUND3 m1, the class of the defect: on every screen of a higher pixel ratio than 1, a dash on a stretched
    non-scaling stroke paints a second dash (the doorway's far leg first, the phone doors' lunettes as dashes). On the
    home, in both scripts, no shape carries both — the verb «stroke» and a non-scaling stroke; the phone doors'
    lunettes are drawn through their own masks, one per door (unique ids, the door's rank). RESTATED under V5.20 (the
    strict test-update rule) for the owner's V5.30 (7 Nov 2026, «geometry saturation», §4 «reduce cumulative
    arches/lines/outlined geometry»; stream A): the ecosystem's doorway and its two masks left with the arch, so the
    page's masks are exactly the four doors' — the same unique-id invariant, and no fifth may return unnoticed.
    RESTATED under V5.20 for the FINAL MICRO-PASS's review (10 Nov 2026, defect 1: on a phone the four lunettes and
    their discs were the page's arches after the hero's door): the doors' seats left with their arches and their masks,
    so the home draws no line through a mask at all — none may return unnoticed — and its four doors still stand."""
    for lang in ("fr", "ar"):
        _response, html = page(f"/{lang}/")
        main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
        both = [tag for tag in _SHAPE.findall(main) if 'data-verb="stroke"' in tag and "non-scaling-stroke" in tag]
        assert both == [], (lang, both)
        assert "passaggio__arco" not in main and "passaggio__seggio" not in main, lang
        assert re.findall(r'<mask id="([^"]+)"', main) == [], lang
        assert main.count('class="passaggio__porta"') == 4, (lang, "the four doors")


def test_final_round_the_arabic_titles_stand_against_their_glyphs_and_the_connector_on_its_rule():
    """QA_ROUND3 M1 and m2 in the home's sheet (the browser half measures them at the eight review widths):
    * the Arabic index's French titles are each the row's remainder, left to right in their own isolate and set against
      their glyph or tile — the end of their own box (the RTL label exception, SECTION_SYSTEM_V2 §2 F);
    * the colophon's connector runs on its folio's 2 px rule: half the folio's line, less half its own pixel.

    v524-cifix (V5.20 strict rule; DL54-189 m2): the old check read the literal `--t-folio-lh: 1rem;` in tokens.css
    and the connector's `0.5rem`. Typography V2 (approved: V5.24 §11–§14, FINAL_DELIVERY_V2 R1, TYPOGRAPHY_V2 §4.2,
    §4.5) made the folio the label role, 16 px in Latin but 20 px in Arabic and under a coarse pointer: the literal half
    stood 2 px above the Arabic rule (the browser twin's three Arabic reds). The intended invariant, on the tokens and
    stronger: the folio's line IS the label role's token, and the connector's offset is half of that same token less
    half a pixel — true in every script and at every pointer, not at one value.

    RESTATED under V5.20 (the strict test-update rule) for the owner's V5.30 (7 Nov 2026, the RULE «a section should not
    stack arch + route line + geometric plate + outlined circle + connector»; stream A): the band's one motif is now the
    Italy + Morocco field, so the library's connector STANDS DOWN on the home — asserted (no offset rule can place it
    again unnoticed), with the folio's role and line held exactly as they were."""
    sheet = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B «l'esploratore»): the index became the explorer — its French titles' rule is the lane's sheet's, the
    # same four declarations on the rail's name and the stage's title
    lane = (ROOT / "static" / "css" / "v5" / "_home-b.css").read_text(encoding="utf-8")
    titles = re.search(
        r'\[dir="rtl"\] \.esplora__voce\[lang\] \.esplora__nome,\s*'
        r'\[dir="rtl"\] \.esplora__titolo\[lang\] \{([^}]*)\}',
        lane,
    )
    assert titles, "the Arabic titles' rule"
    body = " ".join(titles.group(1).split())
    assert body == "flex: 1; direction: ltr; unicode-bidi: isolate; text-align: end;", body
    code = re.sub(r"/\*.*?\*/", "", sheet, flags=re.S)
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026: the campata left the
    # home, its connector with it — none drawn,
    # no rule left that could place it again (stronger than «stands down»)
    ecosystem = (ROOT / "templates" / "pages" / "home" / "_ecosystem.html").read_text(encoding="utf-8")
    assert "campata" not in ecosystem.split("{% endcomment %}", 1)[1], "no campata, no connector"
    assert "campata__ponte" not in code, "and no rule places it again"
    shell = (ROOT / "static" / "css" / "v5" / "_sezioni.css").read_text(encoding="utf-8")
    label = re.search(r"^\.testa__label \{([^}]*)\}", re.sub(r"/\*.*?\*/", "", shell, flags=re.S), flags=re.M)
    assert label and "line-height: var(--t-label-lh);" in label.group(1), "the folio's line is the label role's token"
    own_line = re.search(r"\.colofone__label[^{]*\{[^}]*line-height", code)
    assert not own_line, "the colophon's folio keeps the role's line"
    template = (ROOT / "templates" / "pages" / "home" / "_ecosystem_colophon.html").read_text(encoding="utf-8")
    # V5.24 (FINAL_DELIVERY_V2 §3.4 type; V5.20): the folio carries the label role by name as well (`t-label`)
    assert 'class="testa__label colofone__label t-label"' in template, "the connector's folio is the head's label"


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
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§17, lane A): the pilot's
    # head no longer stands in a seam — its
    # title, lead and call stand on the page's grid at the reading edge in every language (the French title on the
    # Arabic page keeps its own box: the shell's French-run rule), so no centring rule may return; the lead never ends
    # on one word
    lane_sheet = (ROOT / "static" / "css" / "v5" / "_home-a.css").read_text(encoding="utf-8")
    lane = re.sub(r"/\*.*?\*/", "", lane_sheet, flags=re.S)
    assert not re.search(r"pilota__titolo[^{]*\{[^}]*text-align: center", code + lane)
    assert re.search(r"\.pilota__lead \{[^}]*text-wrap: pretty;", lane)
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§19, lane B «la chiarezza»): gate closed, the two surfaces each stand at their own height
    lane_b = (ROOT / "static" / "css" / "v5" / "_home-b.css").read_text(encoding="utf-8")
    assert re.search(r'\.chiaro\[data-trust="interim"\] \{\s*align-items: start;\s*\}', lane_b)


def test_final_review_the_home_reads_the_input_s_modality_in_one_rule(page, seeded, phase3_open):
    """F-M2, lane H's share (§5.3; the first keyboard input): the home's own sheets read the input's modality
    (html[data-input], head.js) in ONE rule — the doors' arrows and arches and the promoter's photograph settling in its
    arch, no duration left to run from the keyboard — each subject filed under a class (never a tag, an :is() or a
    universal subject, which the flip would try against every element). Measured, the home's own rules restyle no
    element at the first key (QA/v522/h/NOTES.md §14); the rest of the flip is the library's and main.css's.
    RESTATED under V5.20 for the FINAL MICRO-PASS's review (10 Nov 2026, defect 1): the doors' arches left with their
    seats, so the one rule's subjects are the doors' arrows and the promoter's photograph — none drawn, none read."""
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
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026: the promoter's photograph
    # no longer settles in a campata — the
    # one rule's subject is the doors' arrows
    assert name == "pages.css" and subjects == ['html[data-input="key"] .passaggio__freccia'], subjects
    assert " ".join(body.split()) == "transition-duration: 0s;", body
    _response, html = page("/fr/")
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    assert main.count('class="icon passaggio__freccia') == 4 and main.count('<svg class="passaggio__arco"') == 0
    assert "campata__media" not in main
