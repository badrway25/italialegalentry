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
    "/fr/le-projet/": ["paper", "paper", "stone", "paper"],
    "/fr/forum/": ["paper", "stone", "night", "stone"],
    "/fr/agami/": ["stone", "night", "stone"],
    "/fr/attention-aux-fraudes/": ["stone"],
    "/fr/reseau/": ["stone"],
    "/fr/contact/": ["stone", "paper"],
    "/fr/vivre-en-italie/": ["stone", "stone"],
}
#: the touches the audit records as a moment's own frame (BACKGROUND_MATERIAL_V2 §5.2: Le projet's story → the panorama
#: that widens — KEEP; FINAL_DELIVERY_V2 §3.6: Vivre KEEP whole, «one ground by decision», QA_ROUND3 m1)
#: (the Vivre panorama is a .sez without data-sec, its «Pour s'installer» band the mosaico: the names the page renders)
ACCEPTED_TOUCHES = {("/fr/le-projet/", "racconto", "panorama"), ("/fr/vivre-en-italie/", "", "mosaico")}
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


# ---- Le projet: the incastro ----------------------------------------------------------------------------------------------
@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_le_projet_s_doors_rise_into_the_volumes(get, lang):
    main = _main(get(f"/{lang}/le-projet/"))
    band = main.select_one('section.projet-porte[data-ground="stone"][data-incastro]')
    assert band is not None
    container = band.select_one(":scope > .container")
    head = container.select_one(":scope > .testa")
    assert head is not None and head.select_one(".testa__rule") is None, (
        "the head is the outline's: no drawn rule over the photograph"
    )
    h2 = head.select_one("h2#project-spaces-title.testa__title.visually-hidden")
    assert h2 is not None and band["aria-labelledby"] == "project-spaces-title"
    # the doors are the band's first visible content
    assert head.find_next_sibling() is container.select_one("ul.mosaico--porte")
    # the panorama's frame stands before it, full bleed (the frame ends on the seam: _projet.css)
    assert main.select_one('[data-sec="panorama"][data-ground="paper"] figure[data-slot="project.volumes"]') is not None


def test_le_projet_s_sheet_ends_the_panorama_on_the_seam_and_keeps_the_statement_at_the_measure():
    css = (APPS / "pages" / "static" / "pages" / "css" / "_projet.css").read_text(encoding="utf-8")
    assert re.search(r"\.projet-panorama\s*\{\s*padding-block-end:\s*0;\s*\}", css)
    assert re.search(r"\.projet-porte \.testa\s*\{\s*margin:\s*0;\s*\}", css)
    for cls in (".projet__enunciato", ".projet__perche"):
        assert re.search(re.escape(cls) + r"\s*\{[^}]*max-inline-size:\s*var\(--measure-body\)", css), cls
    # F-7: the steps' French paragraphs carry their own lead leading on the Arabic page
    assert re.search(r"\.projet-racconto \.racconto__testo > p\[lang\]\s*\{[^}]*line-height:\s*var\(--t-lead-lh\)", css)
    # the caps title one step under its neighbours at the Latin leading (24/30)
    assert re.search(
        r'id="project-why-title"\]:not\(:lang\(ar\)\)\s*\{\s*font-size:\s*1\.5rem;[^}]*line-height:\s*var\(--t-band-lh\)',
        css,
    )
    # the shared doors' drawing is page-only now
    assert ".contatto-porte" not in css


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
    assert re.findall(r'@import url\("([^"]+)"\);', projet) == ["../../css/v5/_materia.css", "_projet.css"]
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
    kinds = contact.select("ul.canali > .canale .canale__kind")  # the telephone channels (the form plate is not one)
    assert kinds and all("t-label" in kind["class"] for kind in kinds)
    source = (TEMPLATES / "pages" / "partials" / "_canali.html").read_text(encoding="utf-8")
    assert source.count('class="canale__kind t-label"') == 2 and source.count("canale__kind") == 2
    assert _main(get(f"/{lang}/reseau/")).select_one("h2.rete__etichetta.t-label#rete-hub-title") is not None
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
    for name in ("_rete.css", "_canali.css", "_contatto.css", "_frodi.css", "_projet.css"):
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
PROJET_CSS_CEILING = 2_222
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
