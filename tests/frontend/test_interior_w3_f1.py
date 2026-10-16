"""
The public interior of design V5.4 — W3-F1, step 1: the doors and the project pages (plan §3.5 item 1; §1.18 D26;
§1.4 RH-5; §1.7 the six-icon ceiling; §1.16; §2.3).

What the grammar promises on every page it draws, read in the rendered HTML: one entrance and one h1; on a door, the
door card for its own audience, carrying the door's way in (the fix pass, M1: the page's one action, or on the
companies' page the way to its form, in the first screen); one primary action at most; at most six icons in the
editorial body (the section device's identity mark apart); no photograph without its caption; the live «who can help
me» line where the page offers an action; no block waiting for a scroll; the page sheets written as plain import lists
in the collected tree; an authority's host beside its link; a locked sentence cut for layout reads back whole (law 8);
French on an Arabic page says so.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.conf import settings

pytestmark = pytest.mark.django_db

ROOT = Path(settings.BASE_DIR)
PAGE = ROOT / "static" / "css" / "v5" / "_pagina.css"
DOORS = {
    "/fr/parcours/": "person",
    "/fr/entreprises/": "company",
    "/fr/institutions/": "institution",
    "/fr/universites-et-formation/": "university",
}
INTERIOR = [
    *DOORS,
    "/fr/projet-pilote/",
    "/fr/forum/",
    "/fr/forum/inscription/",
    "/fr/le-projet/",
    "/fr/agami/",
    "/fr/reseau/",
    "/fr/contact/",
    "/fr/attention-aux-fraudes/",
]
#: pages whose body offers an action, and so says who can help (D26: «who can help me», live text only)
WITH_HELP = ["/fr/parcours/", "/fr/institutions/", "/fr/universites-et-formation/", "/fr/projet-pilote/", "/fr/forum/"]
ICON = re.compile(r'<use href="[^"#]*#icon-([a-z0-9-]+)"')


def _main(html: str) -> str:
    return html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]


@pytest.fixture
def interior(client, seeded, phase3_open, legal_published):
    def get(path: str) -> str:
        response = client.get(path)
        assert response.status_code == 200, (path, response.status_code)
        return response.content.decode("utf-8")

    return get


@pytest.mark.parametrize("path", INTERIOR)
def test_one_entrance_one_h1_and_no_side_column(interior, path):
    main = _main(interior(path))
    assert main.count('<header class="ingresso') == 1, path
    assert main.count("<h1") == 1, path
    assert '<nav class="local-nav"' not in main and "layout-sidebar" not in main, path


#: each door's way in: the control's destination, and whether it is the page's one primary (the companies' card leads
#: to the form further down, whose submit stays the one action)
WAYS = {
    "/fr/parcours/": ("/fr/orientation/", True),
    "/fr/entreprises/": ("#formulaire", False),
    "/fr/institutions/": ("/fr/collaboration/institutions/", True),
    "/fr/universites-et-formation/": ("/fr/collaboration/universites-formation/", True),
}


@pytest.mark.parametrize(("path", "audience"), DOORS.items())
def test_a_door_s_card_carries_its_way_in(interior, path, audience):
    """
    The fix pass (W3-F1's review M1): the door card keeps its night, its disc and its accent rule and carries the
    door's way in — no drawn stair standing in for a photograph. The audience glyph once, from the registry, on its
    disc (decorative); the way's words and its one control on the plate.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(_main(interior(path)), "html.parser")
    entrance = soup.select_one("header.ingresso")
    assert entrance["data-audience"] == audience
    card = entrance.select_one(".ingresso__aside.porta")
    assert card.name == "div" and "on-inverse" in card["class"]
    assert not card.select(".porta__stair") and "aria-hidden" not in card.attrs, (
        "the card is the door's way, not a picture"
    )
    disc = card.select_one(".porta__disc")
    assert disc["aria-hidden"] == "true"
    glyph = {"person": "person", "company": "building", "institution": "institution", "university": "university"}
    assert ICON.findall(str(card)) == [glyph[audience], "arrow"], "the audience glyph once (plan §1.7), the way's arrow"
    assert card.select_one(".via__text").get_text(strip=True), "the way says what it gives"
    url, primary = WAYS[path]
    control = card.select_one(".via__action a.btn")
    assert control["href"] == url
    assert ("btn--primary" in control["class"]) is primary
    primaries = soup.select(".btn--primary")
    if primary:
        assert primaries == [control], "the page's one action is the card's"
    else:
        assert "btn--secondary" in control["class"] and not card.select(".btn--primary")


def test_the_person_door_s_card_is_the_questionnaire_s_action_card(interior):
    from bs4 import BeautifulSoup

    card = BeautifulSoup(_main(interior("/fr/parcours/")), "html.parser").select_one(".porta")
    assert (
        card.select_one("h2.via__title#orientation-title").get_text(strip=True)
        == "Identifiez la voie régulière à explorer"
    )
    assert card.select_one(".via__action a").get_text(" ", strip=True) == "Commencer le questionnaire d’orientation"


def test_how_it_works_stands_on_the_line_and_reads_back_whole(interior):
    """
    The fix pass (W3-F1's review M2; CREATIVE_DIRECTION_V5 law 8, D-U4): the locked «Comment ça marche» sentence is cut
    on its own arrows into four stations of «la linea», its caveat under them; joined back — the hidden opening words
    and arrows included — it is the registry's sentence, character for character.
    """
    from bs4 import BeautifulSoup

    from cms import locked_content

    text = locked_content.text("p3.persons.how_it_works", "fr")
    soup = BeautifulSoup(_main(interior("/fr/parcours/")), "html.parser")
    block = soup.select_one('[data-locked="p3.persons.how_it_works"]')
    assert " ".join(block.get_text(" ").split()) == text
    stations = block.select("ol.linea.linea--across > li.linea__step")
    assert len(stations) == 4 and block.select_one("ol")["data-steps"] == "4"
    labels = [li.select_one(".linea__label").get_text(" ", strip=True) for li in stations]
    assert labels[0].startswith("répondez aux questions") and labels[-1].endswith("acteurs compétents.")
    assert all(li.select_one(".linea__label .visually-hidden") for li in stations[:-1]), "the arrows kept as text"
    assert block.select_one(".how-steps__caveat").get_text(strip=True) == text.rsplit(". ", 1)[1]


def test_the_cut_never_retypes_the_sentence():
    from cms import locked_content
    from pathways import services

    for lang in ("fr", "it", "en", "ar"):
        cut = services.how_it_works(lang)
        assert cut is not None and cut.text == locked_content.get("p3.persons.how_it_works", lang)[0]
        assert len(cut.steps) == 4 and cut.lead.endswith(": ")
        assert cut.lang == ("" if lang == "fr" else "fr")


def test_the_programme_numbers_its_rows_when_not_every_row_has_a_time(interior):
    """CREATIVE_DIRECTION_V5 §20 (the fix pass, m1): a time column only when every row has a time."""
    from bs4 import BeautifulSoup

    from cms import locked_content

    programme = BeautifulSoup(_main(interior("/fr/forum/")), "html.parser").select_one("ol.forum-programme")
    assert "forum-programme--timed" not in programme["class"]
    rows = programme.select(":scope > li")
    assert len(rows) == 8 and all(row.select_one(".forum-programme__num") for row in rows)
    first = rows[0].select_one(".forum-programme__title").get_text()
    assert first == locked_content.get("p2.forum.programme.items", "fr")[0][0], "the first row's words whole"


def test_a_programme_with_every_row_timed_keeps_its_time_column(client, seeded, phase3_open, legal_published):
    from bs4 import BeautifulSoup

    from forum.services import current_event

    event = current_event()
    for index, item in enumerate(event.programme_items.all(), start=1):
        item.time_label = f"{14 + index}h00"
        item.save()
    html = client.get("/fr/forum/").content.decode("utf-8")
    programme = BeautifulSoup(_main(html), "html.parser").select_one("ol.forum-programme")
    assert "forum-programme--timed" in programme["class"]
    assert [t.get_text() for t in programme.select(".forum-programme__time")][:2] == ["15h00", "16h00"]
    assert not programme.select(".forum-programme__num")


def test_french_on_an_arabic_page_says_so(client, seeded, phase3_open, legal_published):
    """WCAG 3.1.2 (the fix pass, m6): the Forum's untranslated eyebrow and name, the trail's link to it, the FAQ's
    question and answer on /ar/agami/ — each carries its language on its own element."""
    from bs4 import BeautifulSoup

    from forum.models import ModeOverride
    from forum.services import current_event

    event = current_event()
    event.mode_override = ModeOverride.PERMANENT
    event.save()
    forum = BeautifulSoup(client.get("/ar/forum/").content, "html.parser")
    assert forum.select_one(".forum-hero__eyebrow").get("lang") == "fr"
    assert forum.select_one("h1.forum-hero__title").get("lang") == "fr"
    register = BeautifulSoup(client.get("/ar/forum/inscription/").content, "html.parser")
    assert register.select_one('.breadcrumbs a[href="/ar/forum/"] span[lang="fr"]')
    french = BeautifulSoup(client.get("/fr/forum/").content, "html.parser")
    assert not french.select_one(".forum-hero__eyebrow").get("lang") and not french.select_one("h1").get("lang")
    agami = BeautifulSoup(client.get("/ar/agami/").content, "html.parser")
    assert agami.select_one("h2#agami-faq-title")["lang"] == "fr"
    assert agami.select_one("p[data-faq]")["lang"] == "fr"


#: the area's template folders (plan §3.5 item 1, «Owns»)
AREA_TEMPLATES = ("pages", "ecosystem", "orientation", "pathways", "forum")


def test_no_template_comment_spans_two_lines():
    """
    The fix pass: Django's `{# … #}` holds on one line only — written over two, it is text, and on /agami/ its words
    stood on the page in both languages. A comment that needs two lines is a {% comment %} block.
    """
    found = []
    for folder in AREA_TEMPLATES:
        for path in sorted((ROOT / "templates" / folder).rglob("*.html")):
            for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
                opened = line.rfind("{#")
                if opened >= 0 and "#}" not in line[opened:]:
                    found.append(f"{path.relative_to(ROOT).as_posix()}:{number}")
    assert not found, found


@pytest.mark.parametrize("lang", ["fr", "ar"])
@pytest.mark.parametrize("path", INTERIOR)
def test_no_template_syntax_reaches_the_page(interior, path, lang):
    main = _main(interior(path.replace("/fr/", f"/{lang}/", 1)))
    for token in ("{#", "#}", "{%", "%}", "{{", "}}"):
        assert token not in main, (path, lang, token)


def test_the_index_and_the_targets_and_the_pilot_s_row_in_the_sheet():
    """
    The fix pass: the entrance's index is one link a row at every width (m3); the forward links' boxes stand on SP-8's
    floor and on 44 px under a finger (A11Y_PERF finding 1); the pilot's eight stations stand in one row only from
    90rem (M5: «ACCOMPAGNEMENT» broke in its middle at 1280 and 1366). The budget pass: the trail is the shared page's
    (v5/_pagina.css §1, W3-F2's drawing) — a 24 px box at rest, its target 44 px under a finger without a taller line.
    """
    css = (ROOT / "static" / "css" / "v5" / "_interior.css").read_text(encoding="utf-8")
    assert "porta__stair" not in css
    assert not re.search(r"\.sommaire__list\s*\{[^}]*flex-wrap", css), "no row of wrapped links"
    floor = re.search(r"\.chapter__more > a,\s*\.chapter__links > a \{([^}]*)\}", css)
    assert floor and "min-block-size: var(--hit-min)" in floor.group(1)
    coarse = css.split("@media (pointer: coarse)", 1)[1].split("}\n}", 1)[0]
    for target in (".chapter__more > a", ".chapter__links > a"):
        assert target in coarse
    assert "min-block-size: var(--hit-primary)" in coarse
    assert ".breadcrumbs" not in re.sub(r"/\*.*?\*/", "", css, flags=re.S), (
        "the trail is drawn once, in the shared page"
    )
    page = re.sub(r"/\*.*?\*/", "", PAGE.read_text(encoding="utf-8"), flags=re.S)
    trail = re.search(r"(?<![\w-])\.breadcrumbs__item a \{([^}]*)\}", page).group(1)
    assert "display: inline-block;" in trail and "padding-block: 2px;" in trail, "a 24 px box, its line 20 px"
    finger = page.split("@media (pointer: coarse)", 1)[1].split("}\n}", 1)[0]
    assert re.search(r"\.breadcrumbs__item a::after \{[^}]*inset-block: -10px;", finger), "44 px under a finger"
    assert re.search(r"\.breadcrumbs__list \{\s*row-gap: var\(--s-5\);", finger), "two rows never overlap"
    for sheet, target in (
        ("apps/pathways/static/pathways/_pathways.css", ".termes__list .tag"),
        ("apps/pages/static/pages/css/_institutional.css", ".contact-address__link"),
    ):
        text = (ROOT / sheet).read_text(encoding="utf-8")
        assert re.search(
            r"@media \(pointer: coarse\) \{\s*" + re.escape(target) + r" \{[^}]*var\(--hit-primary\)", text
        )
    spaces = (ROOT / "apps" / "ecosystem" / "static" / "ecosystem" / "_spaces.css").read_text(encoding="utf-8")
    assert "@media (min-width: 90rem) {\n  .pilot-diagram .linea--across {\n    --linea-cols: 8;" in spaces
    assert "min-width: 80rem" not in spaces


@pytest.mark.parametrize("path", INTERIOR)
def test_one_primary_action_and_at_most_six_icons_in_the_body(interior, path):
    main = _main(interior(path))
    assert len(re.findall(r'class="btn btn--primary\b', main)) <= 1, path
    body_icons = [name for name in ICON.findall(main) if name != "ile-steps"]
    assert len(body_icons) <= 6, (path, body_icons)


@pytest.mark.parametrize("path", INTERIOR)
def test_no_photograph_ships_without_its_caption_and_nothing_waits_for_a_scroll(interior, path):
    main = _main(interior(path))
    assert main.count("<figure") == main.count("<figcaption"), path
    assert not re.search(r'class="[^"]*\breveal\b', main), path


@pytest.mark.parametrize("path", WITH_HELP)
def test_who_can_help_me_is_the_live_line_with_the_public_address(interior, path):
    main = _main(interior(path))
    line = main.split('class="aiuto', 1)[1].split("</p>", 1)[0]
    assert 'href="mailto:contact@agamieuromed.org"' in line, path


def test_the_universities_sentence_is_said_once(interior):
    from cms import locked_content

    main = _main(interior("/fr/universites-et-formation/"))
    assert main.count(locked_content.text("p3.universities.intro", "fr")) == 1


def test_the_pilot_sequence_stands_on_the_line(interior):
    from cms import locked_content

    main = _main(interior("/fr/projet-pilote/"))
    figure = main.split('data-diagram="pilot-sequence"', 1)[1].split("</ol>", 1)[0]
    labels = re.findall(r'<p class="linea__label">(.*?)</p>', figure)
    assert labels == locked_content.get("p3.pilot.sequence", "fr")[0]
    assert "pilot-flow.svg" not in main


def test_an_authority_link_shows_its_host(client, seeded, phase3_open):
    from pathways.models import Pathway

    pathway = Pathway.objects.get(key="salaried_work")
    pathway.authorities = [
        {"name": "Sportello Unico per l'Immigrazione", "url": "https://www.interno.gov.it/", "lang": "it"}
    ]
    pathway.save()
    html = client.get("/fr/parcours/salaried_work/").content.decode("utf-8")
    row = _main(html).split('class="registro registro--words authority-list"', 1)[1].split("</ul>", 1)[0]
    assert 'href="https://www.interno.gov.it/"' in row
    assert '<span class="autorita__host">interno.gov.it</span>' in row


def test_the_pathway_sheet_has_its_index_in_the_entrance_and_no_sticky_bar(client, seeded, phase3_open):
    html = client.get("/fr/parcours/salaried_work/").content.decode("utf-8")
    entrance = _main(html).split('<header class="ingresso', 1)[1].split("</header>", 1)[0]
    for anchor in ("apercu", "etapes", "documentation", "autorites", "avertissements", "ressources", "orientation"):
        assert f'href="#{anchor}"' in entrance
    assert "section-nav" not in html


@pytest.mark.parametrize(
    ("sheet", "imports"),
    [
        (
            "apps/ecosystem/static/ecosystem/ecosystem.css",
            [
                "../css/v5/_pagina.css",
                "../css/v5/_interior.css",
                "../css/v5/_journey-passage.css",
                "../css/v5/_porta.css",
                "_spaces.css",
            ],
        ),
        ("apps/forum/static/forum/forum.css", ["../css/v5/_pagina.css", "../css/v5/_interior.css", "_forum.css"]),
        (
            "apps/pages/static/pages/css/interior.css",
            ["../../css/v5/_pagina.css", "../../css/v5/_interior.css", "_institutional.css"],
        ),
        (
            "apps/pathways/static/pathways/pathways.css",
            [
                "../css/v5/_pagina.css",
                "../css/v5/_interior.css",
                "../css/v5/_journey-passage.css",
                "../css/v5/_porta.css",
                "_pathways.css",
            ],
        ),
    ],
)
def test_page_sheets_are_plain_import_lists_in_the_collected_tree(sheet, imports):
    """Each page sheet is a list of imports a later family extends with one line (W3-D's passage; DS 2026 §2)."""
    text = (ROOT / sheet).read_text(encoding="utf-8")
    without_comments = re.sub(r"/\*.*?\*/", "", text, flags=re.S).strip()
    assert re.findall(r'@import url\("([^"]+)"\);', without_comments) == imports
    assert re.sub(r'@import url\("[^"]+"\);', "", without_comments).strip() == "", "nothing but imports"


def test_the_interior_grammar_never_enters_main_css():
    main = (ROOT / "static" / "css" / "main.css").read_text(encoding="utf-8")
    assert "_interior.css" not in main and "_porta.css" not in main and "_pagina.css" not in main


#: the components every page of the public interior draws — one drawing each, in the shared page (the owner's V5.8:
#: no duplicated component families; W3-F2's review m11), never again in a surface's own partial
SHARED_RULES = (
    ".breadcrumbs__item a {",
    ".breadcrumbs__item[aria-current] {",
    ".ingresso,\n.page-header {",
    ".ingresso__title,\n.page-header__title {",
    ".ingresso__lead,\n.page-header__lead {",
    ".chapter__inner {",
    ".chapter__mark {",
    ".chapter__title,\n.chapter__head > h2:not([class]) {",
    ".chapter__label {",
    ".registro {",
    ".registro__row {",
    ".registro__text {",
    ".autorita__host {",
    ".figura img {",
    ".aiuto {",
)


def test_one_page_partial_draws_the_interior_s_shared_components_for_both_families():
    """The budget pass: W3-F1's _interior.css and W3-F2's _lettura.css drew the trail, the head, the chapters, the
    register and D26's shared slots value for value; they are drawn once, in static/css/v5/_pagina.css, the first
    import of both families' page sheets, and neither partial draws them again."""
    page = re.sub(r"/\*.*?\*/", "", PAGE.read_text(encoding="utf-8"), flags=re.S)
    own = {
        name: re.sub(r"/\*.*?\*/", "", (ROOT / "static" / "css" / "v5" / name).read_text(encoding="utf-8"), flags=re.S)
        for name in ("_interior.css", "_lettura.css")
    }
    for rule in SHARED_RULES:
        assert len(re.findall(r"(?m)^" + re.escape(rule), page)) == 1, rule
        for name, css in own.items():
            head = rule.split(",")[0].split(" {")[0]
            assert not re.search(r"(?m)^\s*" + re.escape(head) + r"\s*[,{]", css), (name, head)
    importers = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "apps").glob("*/static/**/*.css")
        if "_pagina.css" in path.read_text(encoding="utf-8")
    )
    assert importers == [
        "apps/cms/static/cms/lettura.css",
        "apps/ecosystem/static/ecosystem/ecosystem.css",
        "apps/forum/static/forum/forum.css",
        "apps/orientation/static/orientation/wizard.css",
        "apps/pages/static/pages/css/interior.css",
        "apps/pathways/static/pathways/pathways.css",
    ]
    for path in importers:
        imports = re.findall(r'@import url\("([^"]+)"\);', (ROOT / path).read_text(encoding="utf-8"))
        assert imports[0].endswith("css/v5/_pagina.css"), (path, "the shared page first, then the surface's own")
    assert not re.search(r"#[0-9a-fA-F]{3,8}\b|rgba?\(|gradient\(", page), "tokens only"
    assert not re.search(r"(?<![\w-])(margin|padding|border)-(left|right|top|bottom)\s*:", page), "logical only"
    tokens = (ROOT / "static" / "css" / "v5" / "tokens.css").read_text(encoding="utf-8")
    declared = set(re.findall(r"(--[a-z0-9-]+)\s*:", tokens + page))
    assert set(re.findall(r"var\((--[a-z0-9-]+)", page)) <= declared


def test_the_door_card_loads_only_where_a_door_is_drawn():
    """
    The fix pass (V5.8: a surface's own CSS loads only where it is drawn): the door card and its way in are the doors'
    own — static/css/v5/_porta.css, imported by the two door sheets alone; the interior's grammar, which the Forum,
    the project's pages and the questionnaire load too, carries none of it.
    """
    source = (ROOT / "static" / "css" / "v5" / "_interior.css").read_text(encoding="utf-8")
    interior = re.sub(r"/\*.*?\*/", "", source, flags=re.S)
    assert not re.search(r"\.porta\b|\.via__|\.ingresso__way", interior)
    importers = sorted(
        path.relative_to(ROOT).as_posix()
        for path in (ROOT / "apps").glob("*/static/**/*.css")
        if "_porta.css" in path.read_text(encoding="utf-8")
    )
    assert importers == ["apps/ecosystem/static/ecosystem/ecosystem.css", "apps/pathways/static/pathways/pathways.css"]
