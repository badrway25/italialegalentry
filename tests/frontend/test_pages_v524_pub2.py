"""
V5.24 — the professional pass on the system, trust and reading pages, lane PUB2 (FINAL_DELIVERY_V2 §3.6; BACKGROUND_MATERIAL_V2
§3.2, §3.3, §5.2; TYPOGRAPHY_V2 §4.2, §6, F-3, F-4, F-7, F-8; IMAGERY_ATTRIBUTION D4; ARABIC_AUDIT 02_class_b_wraps W1.2, W1.3,
W5.3; label v524-pub2-build): what the server renders. The browser half is tests/frontend/test_pages_browser_v524_pub2.py.

  * the grounds the audit decided, on the pages' markup: the FAQ explorer, the glossary register, the term page's scheda,
    the Forum's «dal dialogo ai progetti», AGAMI's identity band and the fraud page's one band on STONE; the two «il rimando»
    strips on PAPER; no two neighbouring V2 sections of one kind (stone and pietra being one) but the two touches the
    audit records as a moment's own frame;
  * the two seams: Le projet's «incastro» (data-incastro on the doors' band, the doors its first content, the head the
    outline's) and the Forum's «raccordo» (the span the first child of the band it enters, the draw-y verb, aria-hidden);
  * the material partial page-only, reached through the Forum's sheet and Le projet's new route sheet — never through
    main.css, the shared interior sheet or the reading pages' sheet (R4 a: the Réseau and AGAMI totals);
  * the label role by name on the FAQ's category, AGAMI's registers, the Réseau hub and the contact channels' kind (F-3,
    F-4), the letters of the glossary at the display weight, the French step paragraphs of Le projet with their own
    leading (F-7) and the statement column at the reading measure (F-8);
  * PX's guard on the Forum's two bylines; AR's wordings (the Forum eyebrow a team string without a French branch, the
    theme page's sentence) and the «Privacy Policy» run isolated in the FAQ's links (W5.3);
  * the budgets: the new route sheet at its measure, Le projet's page total under the interior letter (the other totals are
    tests/frontend/test_frontispiece_v515_c.py's).
"""

from __future__ import annotations

import gzip
import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.utils import translation
from django.utils.translation import gettext

ROOT = Path(__file__).resolve().parents[2]
STATIC = ROOT / "static"
TEMPLATES = ROOT / "templates"
APPS = ROOT / "apps"

pytestmark = pytest.mark.compliance

#: the page → the grounds of its V2 sections in order (the frontispiece is not a .sez: the head's paper is the audit's premise)
GROUNDS = {
    "/fr/faq/": ["stone", "paper"],
    "/fr/glossaire/": ["stone", "paper"],
    "/fr/glossaire/nulla_osta/": ["stone"],
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: Le projet is «la carta» —
    # the thesis on paper, «Pourquoi» on stone, the bearer on paper, the spaces on night, the foot on paper (five
    # bands, still no two neighbours of one kind, now with no accepted touch: the story/panorama pair left)
    "/fr/le-projet/": ["paper", "stone", "paper", "night", "paper"],
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D):
    # the audience band left the night for the paper (one night per page: the head's) — still no two neighbours alike
    "/fr/forum/": ["paper", "stone", "paper", "stone"],
    "/fr/agami/": ["stone", "night", "stone"],
    "/fr/attention-aux-fraudes/": ["stone"],
    "/fr/reseau/": ["stone"],
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D,
    # «lo sportello»): the page composes no library section any more — its desk and its doors are its own blocks, held to
    # the same rule (two grounds, never alike side by side) by test_the_contact_desk_and_its_doors_stand_on_two_grounds
    "/fr/contact/": [],
    "/fr/vivre-en-italie/": ["stone", "stone"],
}
#: the touches the audit records as a moment's own frame (BACKGROUND_MATERIAL_V2 §5.2: Le projet's story → the panorama
#: that widens — KEEP; FINAL_DELIVERY_V2 §3.6: Vivre KEEP whole, «one ground by decision», QA_ROUND3 m1)
#: (the Vivre panorama is a .sez without data-sec, its «Pour s'installer» band the mosaico: the names the page renders)
ACCEPTED_TOUCHES = {("/fr/vivre-en-italie/", "", "mosaico")}
ONE_KIND = {"stone": "stone", "pietra": "stone"}


@pytest.fixture
def get(client, seeded, phase3_open, legal_published):
    def fetch(path: str) -> str:
        response = client.get(path)
        assert response.status_code == 200, (path, response.status_code)
        return response.content.decode("utf-8")

    return fetch


def _main(html: str) -> BeautifulSoup:
    return BeautifulSoup(html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0], "html.parser")


def _gz(relative: str) -> int:
    return len(gzip.compress((STATIC / relative).read_bytes(), 9))


# ---- the grounds and the adjacency rule ------------------------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize("path", list(GROUNDS))
def test_the_grounds_the_audit_decided_and_no_two_neighbours_of_one_kind(get, path):
    sections = [s for s in _main(get(path)).select(".sez[data-ground]") if s.find_parent(class_="sez") is None]
    grounds = [s["data-ground"] for s in sections]
    assert grounds == GROUNDS[path], (path, grounds)
    for before, after in zip(sections, sections[1:]):
        pair = (path, before.get("data-sec", ""), after.get("data-sec", ""))
        if pair in ACCEPTED_TOUCHES:
            continue
        assert ONE_KIND.get(before["data-ground"], before["data-ground"]) != ONE_KIND.get(
            after["data-ground"], after["data-ground"]
        ), pair


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_contact_desk_and_its_doors_stand_on_two_grounds(get, lang):
    """RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D, «lo sportello»;
    replaces the contact page's entry of GROUNDS, ["stone", "paper"]): the desk stands on the stone of the area surface,
    the three doors after it on the page's paper — the two blocks are neighbours, and of two kinds."""
    main = _main(get(f"/{lang}/contact/"))
    desk = main.select_one("section.sportello")
    assert desk is not None and desk.find_next_sibling() is main.select_one("section.sportello-mirate")
    css = re.sub(
        r"/\*.*?\*/",
        "",
        (APPS / "pages" / "static" / "pages" / "css" / "_contatto-v532.css").read_text(encoding="utf-8"),
        flags=re.S,
    )
    assert re.search(r"(?m)^\.sportello \{[^}]*background: var\(--surface-area\);", css)
    doors = re.search(r"(?m)^\.sportello-mirate \{([^}]*)\}", css).group(1)
    assert "background" not in doors, "the doors stand on the page's paper"


# ---- Le projet: «la carta» -----------------------------------------------------------------------------------------------
# RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the incastro (the doors' arched tops over a text-less
# panorama) left with the arches — the owner's lesson list: no geometry as decoration, no list said twice. Restated with
# the same subjects and stronger content: the volumes' frame now stands BESIDE the words it argues for, the four spaces
# are real links with a visible title, and the steps keep their anchors.
@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_le_projet_s_spaces_are_a_titled_index_of_real_links_and_the_volumes_argue_the_why(get, lang):
    main = _main(get(f"/{lang}/le-projet/"))
    band = main.select_one('section.projet-spazi[data-ground="night"][aria-labelledby="project-spaces-title"]')
    assert band is not None and not band.select("[data-incastro], svg.mosaico__arco, .mosaico--porte")
    h2 = band.select_one("h2#project-spaces-title")
    assert h2 is not None and "visually-hidden" not in h2.get("class", [])
    links = band.select("ul.projet-spazi__lista > li.projet-spazio[data-audience] > a.projet-spazio__link[href]")
    assert len(links) == 4 and all(a.select_one(".projet-spazio__nome").get_text(strip=True) for a in links)
    assert all(a.select_one(".sez-disc[aria-hidden='true'] svg") for a in links)
    # the volumes beside «Pourquoi», in its band, after its words
    why = main.select_one('section.projet-perche-band#project-why[data-ground="stone"]')
    assert why.select_one("h2#project-why-title") is not None
    frame = why.select_one('figure[data-slot="project.volumes"]')
    assert frame is not None and frame.find_previous_sibling(class_="projet-perche-band__testo") is not None
    assert main.select_one("#project-promoter h2#project-promoter-title") is not None
    assert not main.select(".racconto, .sistema__nodi, [data-sec='panorama']"), "the figure and the panorama left"


def test_le_projet_s_sheet_keeps_the_reading_measure_and_the_latin_leading():
    css = (APPS / "pages" / "static" / "pages" / "css" / "_projet.css").read_text(encoding="utf-8")
    for cls in (".projet__perche", ".projet-chi__testo > p:not(.projet__oltre)"):
        assert re.search(re.escape(cls) + r"\s*\{[^}]*max-inline-size:\s*var\(--measure-body\)", css), cls
    # the statement: at most 34 em, the band size and its own leading
    assert re.search(r"\.projet__enunciato\s*\{[^}]*max-inline-size:\s*34em;", css)
    # F-7: a French paragraph on the Arabic page carries its own Latin leading
    assert re.search(r"\.projet-tesi__testo > p\[lang\]\s*\{[^}]*line-height:\s*var\(--t-band-lh\)", css)
    # the caps title one step under its neighbours at the Latin leading, never on an Arabic title
    assert re.search(
        r'id="project-why-title"\]:not\(:lang\(ar\)\)\s*\{\s*font-size:\s*var\(--t-band\);[^}]*line-height:\s*var\(--t-band-lh\)',
        css,
    )
    assert ".contatto-porte" not in css and "incastro" not in css.split("*/", 1)[1] and "arco" not in css


# ---- the Forum: the raccordo ----------------------------------------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_no_raccordo_enters_the_forum_s_story_band(get, lang):
    """V5.30 Fast Visual Variety Correction §5 (V5.20 strict rule): the line between the pair and the story is gone; the two
    bands stand side by side as they did."""
    main = _main(get(f"/{lang}/forum/"))
    band = main.select_one('section.forum-filo[data-ground="stone"]')
    assert not band.select(".sez-raccordo")
    assert main.select_one('section.forum-pair[data-ground="paper"]').find_next_sibling() is band


def test_the_forum_s_sheet_places_the_raccordo_on_the_station_axis_from_64rem():
    css = (APPS / "forum" / "static" / "forum" / "_forum.css").read_text(encoding="utf-8")
    assert re.search(
        r"\.forum-filo > \.sez-raccordo\s*\{[^}]*--risalita:\s*clamp\(var\(--s-8\), 4vw, var\(--s-12\)\)", css
    )
    assert re.search(r"--sez-raccordo:\s*calc\(var\(--risalita\) \+ clamp\(var\(--s-16\), 8vw, var\(--s-24\)\)\)", css)
    assert "* 5 / 12 + var(--s-16) + 11px" in css, "the second column's start plus the station rings' axis"
    assert re.search(
        r"\.forum-filo__obiettivi > \.forum-titolo\s*\{\s*padding-inline-start:\s*var\(--s-12\);\s*\}", css
    )
    assert ".forum-cta__actions" not in css and ".forum-action," not in css, (
        "the dead rule and selector (coverage, NOTES §6)"
    )


# ---- the material partial is page-only -----------------------------------------------------------------------------------
def test_the_material_partial_reaches_the_pages_through_their_route_sheets_only():
    forum = (APPS / "forum" / "static" / "forum" / "forum.css").read_text(encoding="utf-8")
    projet = (APPS / "pages" / "static" / "pages" / "css" / "projet.css").read_text(encoding="utf-8")
    assert re.findall(r'@import url\("([^"]+)"\);', forum) == [
        "../css/v5/_pagina.css",
        "../css/v5/_interior.css",
        "../css/v5/_sezioni.css",
        "../css/v5/_sigillo.css",
        "../css/v5/_materia.css",
        "_forum.css",
    ]
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: Le projet no longer draws a
    # material recipe (the incastro left), so its route sheet carries its own rules only — the partial reaches the Forum alone
    assert re.findall(r'@import url\("([^"]+)"\);', projet) == ["_projet.css"]
    for sheet in (
        "static/css/main.css",
        "apps/pages/static/pages/css/interior.css",
        "apps/cms/static/cms/lettura.css",
        "apps/cms/static/cms/lessico.css",
        "apps/cms/static/cms/faq.css",
    ):
        assert "_materia.css" not in (ROOT / sheet).read_text(encoding="utf-8"), sheet
    assert "_projet.css" not in (APPS / "pages" / "static" / "pages" / "css" / "interior.css").read_text(
        encoding="utf-8"
    )
    project = (TEMPLATES / "pages" / "project.html").read_text(encoding="utf-8")
    assert "{% static 'css/dist/pages/css/projet.css' %}" in project


# ---- the type roles ------------------------------------------------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_labels_carry_the_role_by_name(get, lang):
    agami = _main(get(f"/{lang}/agami/"))
    assert agami.select_one("h2.agami-id__etichetta.t-label#agami-contact-title") is not None
    assert agami.select(".agami-id__voce > dt") and all(
        "t-label" in dt["class"] for dt in agami.select(".agami-id__voce > dt")
    )
    assert len(agami.select("dt.agami-id__etichetta-voce.t-label")) == 2
    assert agami.select_one('section.agami-identita[data-ground="stone"]') is not None
    contact = _main(get(f"/{lang}/contact/"))
    # every channel drawn carries the role (WhatsApp is drawn only where its number is configured — V5.19 option B);
    # the partial's two kinds both carry it in the source
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D,
    # «lo sportello»): the channels are the desk's rows — the address's, then the two voices' — and every kind drawn,
    # and every kind in the source (the page carries its channels itself: pages/partials/_canali.html left), carries it;
    # the head's one label too, on the contact page and on the form's own page
    kinds = contact.select("ul.sportello__lista > .sportello-canale .sportello-canale__tipo")
    assert kinds and all("t-label" in kind["class"] for kind in kinds)
    source = (TEMPLATES / "pages" / "contact.html").read_text(encoding="utf-8")
    assert source.count('class="sportello-canale__tipo t-label"') == 3 and source.count("sportello-canale__tipo") == 3
    assert "t-label" in contact.select_one("header.sportello-testa p.sportello-testa__label")["class"]
    form_page = _main(get(f"/{lang}/contact/formulaire/"))
    assert all("t-label" in p["class"] for p in form_page.select(".sportello-testa__label, .sportello-canale__tipo"))
    # (lane D, «l'esploratore») RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION
    # directive of 12 Nov 2026: P2-4 of the integration review — «En bref» and its prescribed statement are Le projet's,
    # linked from the head, never repeated; the head's one label is its folio, by name: exactly one, the section's words
    labels = _main(get(f"/{lang}/reseau/")).select("header.rete-testa .t-label")
    assert [(label.name, label["class"][0]) for label in labels] == [("p", "rete-testa__label")]
    with translation.override(lang):
        assert labels[0].get_text(strip=True) == gettext("Le projet")
    fraud = _main(get(f"/{lang}/attention-aux-fraudes/"))
    assert "t-label" in fraud.select_one("header.avvertenza-testa p.avvertenza-testa__label")["class"]
    # FINAL MICRO-PASS §6 B1 (V5.20; was «the explorer's category heading carries the label role»): the explorer and its
    # category heading left — the list is named by its heading for assistive technology, and the one label the FAQ
    # still draws (the empty search's register) carries the role by name
    faq = _main(get(f"/{lang}/faq/"))
    assert faq.select_one(".faq-esploratore__categoria, .faq-esploratore") is None
    assert faq.select_one("section#questions h2#faq-domande-title.visually-hidden") is not None
    empty = _main(get(f"/{lang}/faq/?q=zzzz-aucun"))
    assert "t-label" in empty.select_one("h3#faq-index-title.faq-vuoto__titolo")["class"]


def test_the_sheets_read_the_roles_and_the_steps():
    agami = (APPS / "pages" / "static" / "pages" / "css" / "_agami.css").read_text(encoding="utf-8")
    assert "var(--f-mono)" not in agami
    assert not re.search(r"font-size:\s*(clamp|min|max)\(", re.sub(r"/\*.*?\*/", "", agami, flags=re.S))
    assert "cqi" not in agami, "the address takes the steps by container query"
    assert re.search(
        r"@container \(min-width: 24rem\)\s*\{\s*\.agami-id__indirizzo\s*\{\s*font-size:\s*var\(--t-band\)", agami
    )
    assert "background-color: var(--surface-raised)" in agami, "the colonnade plate's face raised on the stone band"
    frodi = (APPS / "pages" / "static" / "pages" / "css" / "_frodi.css").read_text(encoding="utf-8")
    assert "cqi" not in frodi and re.search(r"@container \(min-width: 18rem\)\s*\{\s*\.frodi__indirizzo", frodi)
    lessico = (APPS / "cms" / "static" / "cms" / "_lessico-v2.css").read_text(encoding="utf-8")
    # FINAL MICRO-PASS §6 B2 (V5.20; was the letter at the display weight): a modest letter heading — the entry's step,
    # the title's weight, the accent ink; no giant letter
    assert re.search(
        r"\.lessico__lettera\s*\{[^}]*font-size:\s*var\(--t-entry\);[^}]*font-weight:\s*var\(--w-title\);[^}]*color:\s*var\(--accent-text\)",
        lessico,
    )
    assert "foto__credit" not in lessico, "the panorama's credit rule (PX, IMAGERY_ATTRIBUTION D3)"
    assert re.search(
        r"\.page-glossary-term \[data-fronte\]\[data-compact\] \.ingresso__title\s*\{[^}]*font-size:\s*var\(--t-display\)",
        lessico,
    )
    # FINAL MICRO-PASS §6 B2 (V5.20; was the term page's outlined initial at four and a half display steps): it left
    assert "scheda__iniziale" not in lessico and "calc(var(--t-display) * 4.5)" not in lessico
    assert ":lang(ar) :is(" not in lessico, "the Arabic rule in the subject form"
    for name in ("_faq-v2.css",):
        sheet = (APPS / "cms" / "static" / "cms" / name).read_text(encoding="utf-8")
        assert "var(--f-mono)" not in sheet and "text-transform: uppercase" not in sheet
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D): the contact
    # desk's partial is held to the same rules (stronger: one more sheet)
    for name in ("_rete.css", "_canali.css", "_contatto.css", "_contatto-v532.css", "_frodi.css", "_projet.css"):
        sheet = re.sub(
            r"/\*.*?\*/",
            "",
            (APPS / "pages" / "static" / "pages" / "css" / name).read_text(encoding="utf-8"),
            flags=re.S,
        )
        assert "var(--f-mono)" not in sheet and "text-transform: uppercase" not in sheet, name
        assert not re.search(r"font-size:\s*(clamp|min|max)\(", sheet), name
        assert not re.search(
            r':lang\(ar\)\s+[.\[a-z:]|\[dir="rtl"\]\s+[^{]*\{[^}]*(line-height|letter-spacing|font-size)', sheet
        ), (name, "the Arabic rules in the subject form")


# ---- PX's guard and AR's wordings --------------------------------------------------------------------------------------
def test_the_forum_bylines_render_only_when_the_licence_demands_it_and_the_eyebrow_is_a_team_string():
    hero = (TEMPLATES / "forum" / "partials" / "hero.html").read_text(encoding="utf-8")
    assert "{% if event.hero_image.attribution_required %}" in hero and "{% if event.hero_image.credit %}" not in hero
    assert 'translate "Dialogue institutionnel permanent"' in hero
    assert (
        "Espace permanent de dialogue et de coopération" not in hero
        and 'lang="fr"' not in hero.split("forum-hero__eyebrow", 1)[1].split("\n", 1)[0]
    )
    gallery = (TEMPLATES / "forum" / "partials" / "permanent_sections.html").read_text(encoding="utf-8")
    assert "{% if media.attribution_required %}" in gallery and "{% if media.credit %}" not in gallery
    topic = (TEMPLATES / "living" / "topic.html").read_text(encoding="utf-8")
    assert "repères pratiques pour s’installer et vivre au quotidien en Italie." in topic
    assert "fiches pratiques pour accompagner l’intégration" not in topic


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_privacy_policy_is_an_isolated_english_run_in_the_faq_s_links(get, lang):
    html = get(f"/{lang}/faq/")
    assert '<span lang="en" dir="ltr">Privacy Policy</span>' in html
    assert re.search(
        r'<a class="faq-chip" href="/'
        + lang
        + r'/privacy-policy/">[^<]*<span lang="en" dir="ltr">Privacy Policy</span>',
        html,
    )


# ---- budgets -------------------------------------------------------------------------------------------------------------
#: the new route sheet's ceiling, at its measure (gzip -9 of the built dist; V5.20 — a new sheet, a new ceiling; CLOSING ratchets)
#: V5.29 (stream SYS's weight-map contract, §3: _projet.css's literal 500 / 600 on --w-title / --w-strong, value-identical):
#: 2 219 → 2 222 at the measure (NOTES «ceilings re-recorded»)
# RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the sheet lost the material
# partial and the story's figure — the ceiling ratchets DOWN to the new measure (1 341 B) + 3 %
PROJET_CSS_CEILING = 1_382
FORM_SHEETS = {"css/dist/core/forms.css", "css/dist/core/steps.css", "css/dist/core/glyph.css"}
STYLESHEET = re.compile(r'<link rel="stylesheet" href="/static/(css/dist/[^"?]+\.css)[^"]*"')


def test_le_projet_s_route_sheet_is_inside_its_ceiling():
    assert _gz("css/dist/pages/css/projet.css") <= PROJET_CSS_CEILING, _gz("css/dist/pages/css/projet.css")


@pytest.mark.django_db
def test_le_projet_stays_inside_the_interior_total(get):
    sheets = sorted(set(STYLESHEET.findall(get("/fr/le-projet/"))))
    assert "css/dist/pages/css/projet.css" in sheets and "css/dist/pages/css/interior.css" in sheets, sheets
    total = sum(_gz(sheet) for sheet in sheets if sheet not in FORM_SHEETS)
    assert total <= 56_320, (total, sheets)
