"""
V5.32 GLOBAL SITE + PLATFORM DESIGN COMPLETION (the owner's directive of 12 Nov 2026), lane D — knowledge, trust and
network: what the lane's public pages now promise, rendered by the server, and the measured budgets of its new bundles
(gzip -9 — Python ``gzip.compress(b, 9)`` of the dist file; each ceiling the measure rounded up, at most + 3 %).

  * Contact «lo sportello»: the channels desk (the address with its copy action, the freephone and WhatsApp rows from
    the site's settings only) beside the enquiries app's own form, posted to the enquiries view — or, while gate G2 is
    closed, the G2 notice in the form's seat; the page links its own sheet and script only;
  * Fraudes «l'avvertenza»: the prescribed statement whole in ONE amber panel, given its hierarchy by its own sentences
    (cms.locked_split «sentence»: the words and their order unchanged) — never restated in team words; beside it the
    home band's list of signs, carried whole (P1-2 of the integration review: the same msgids, the same symbols);
  * Réseau «l'esploratore»: the five actors as a tablist on complete markup (every panel in the page without script),
    no ring, spoke or flag drawn;
  * FAQ: the guide beside the list — the search, the themes and the help card (the one way to a person; the foot no
    longer repeats it);
  * the public Forum: its own public sheet (lane E's forum/forum.css stays the platform's), the local nav a scroll spy
    over sections that exist, no seal drawn in the head;
  * no page of the lane links the frontispiece's sheet any more (none draws it).
The browser half (the copy action, the tablist's keys, the FAQ's filter) was verified in headed Chrome (lane D's
NOTES.md); the shared runtimes keep their own browser tests (tests/frontend/test_pages_browser_v522_p2.py).
"""

from __future__ import annotations

import gzip
import re
from pathlib import Path

import pytest
from bs4 import BeautifulSoup
from django.conf import settings
from django.utils import translation
from django.utils.translation import gettext

from cms import locked_content

ROOT = Path(settings.BASE_DIR)
STATIC = ROOT / "static"

#: the lane's new bundles: dist file → ceiling in bytes (gzip -9), measured on 12 Nov 2026 and rounded up (≤ + 3 %)
NEW_BUNDLES = {
    "css/dist/pages/css/contatto.css": 1_870,  # measured 1 854 — «lo sportello» + the trail's rules copied from _pagina
    "css/dist/forum/pubblico.css": 5_680,  # measured 5 540 — the public Forum's own sheet (pagina, interior, sezioni, page)
    "js/dist/contatto.js": 418,  # measured 406 — the address's copy action
}
STYLESHEET = re.compile(r'<link rel="stylesheet" href="/static/(css/dist/[^"?]+\.css)[^"]*"')
SCRIPT = re.compile(r'<script type="module" src="/static/(js/dist/[^"?]+\.js)[^"]*"')
#: the lane's pages and the one sheet each adds to the site's (main, reveal, portico)
ROUTE_SHEETS = {
    "/fr/contact/": ["css/dist/pages/css/contatto.css", "css/dist/core/forms.css"],
    "/fr/contact/formulaire/": ["css/dist/pages/css/contatto.css", "css/dist/core/forms.css"],
    "/fr/faq/": ["css/dist/cms/lettura.css", "css/dist/cms/faq.css"],
    "/fr/glossaire/": ["css/dist/cms/lettura.css", "css/dist/cms/lessico.css"],
    "/fr/vivre-en-italie/": ["css/dist/cms/lettura.css", "css/dist/cms/lessico.css"],
    "/fr/reseau/": ["css/dist/pages/css/interior.css", "css/dist/pages/css/rete.css"],
    "/fr/attention-aux-fraudes/": ["css/dist/pages/css/interior.css", "css/dist/pages/css/frodi.css"],
    "/fr/forum/": ["css/dist/forum/pubblico.css"],
}
SITE_SHEETS = ["css/dist/main.css", "css/dist/core/reveal.css", "css/dist/core/portico.css"]
#: the premium forms' own sheets: the form's tag (apps/core, ile_forms) links them where the form stands, in the body
FORM_SHEETS = {"css/dist/core/forms.css", "css/dist/core/steps.css", "css/dist/core/glyph.css"}


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


def test_the_lane_s_new_bundles_hold_their_measured_ceilings():
    for relative, ceiling in NEW_BUNDLES.items():
        assert _gz(relative) <= ceiling, (relative, _gz(relative), ceiling)
    # page-only: never through the site's sheet
    main_css = (STATIC / "css" / "main.css").read_text(encoding="utf-8")
    assert "_contatto-v532.css" not in main_css and "_forum-pubblico.css" not in main_css
    entry = (ROOT / "apps" / "pages" / "static" / "pages" / "css" / "contatto.css").read_text(encoding="utf-8")
    assert re.findall(r'@import url\("([^"]+)"\);', entry) == ["_contatto-v532.css"]
    public = (ROOT / "apps" / "forum" / "static" / "forum" / "pubblico.css").read_text(encoding="utf-8")
    assert "_forum.css" not in public, "the platform's sheet (lane E's) is never pulled into the public one"


@pytest.mark.django_db
@pytest.mark.parametrize("path", list(ROUTE_SHEETS))
def test_each_page_links_the_site_s_sheets_then_its_own_and_never_the_frontispiece(get, path):
    html = get(path)
    head = html.split("</head>", 1)[0]
    sheets = STYLESHEET.findall(html)
    assert sheets == SITE_SHEETS + ROUTE_SHEETS[path], (path, sheets)
    assert all(sheet in head for sheet in sheets if sheet not in FORM_SHEETS), "every page sheet in the <head>"
    assert "css/dist/pages/css/fronte.css" not in html and "data-fronte" not in html
    scripts = SCRIPT.findall(html)
    assert ("js/dist/contatto.js" in scripts) == (path == "/fr/contact/"), (path, scripts)


@pytest.mark.django_db
def test_the_contact_desk_says_its_channels_from_the_settings_only(client, seeded, whatsapp_channel):
    html = client.get("/fr/contact/").content.decode("utf-8")
    main = _main(html)
    rows = main.select(".sportello__canali ul.sportello__lista > li.sportello-canale")
    assert len(rows) == 3
    address = rows[0].select_one("a.email#contact-address")
    assert address["href"] == "mailto:contact@agamieuromed.org" and address.get_text() == "contact@agamieuromed.org"
    # the copy action: hidden until the script finds the Clipboard API, its words the page's own, its result announced
    copy = rows[0].select_one('button.sportello-copia[type="button"][data-copia="contact-address"][hidden]')
    assert copy is not None and copy["data-copia-fatto"] and copy.select_one("[data-copia-testo]").get_text().strip()
    assert rows[0].select_one('[role="status"][data-copia-stato]') is not None
    # the two telephone channels: the settings' values, each number one left-to-right unit, named for a screen reader
    tels = [a["href"] for a in main.select('.sportello__canali a[href^="tel:"]')]
    assert tels == ["tel:800642015"]
    whatsapp = main.select_one(f'.sportello__canali a[href="{whatsapp_channel.url}"]')
    assert whatsapp is not None and whatsapp.select_one('bdi.phone[dir="ltr"]').get_text() == whatsapp_channel.label
    assert whatsapp_channel.label in whatsapp["aria-label"]
    # no template of the desk writes a number or a WhatsApp address (they live in the settings only)
    for name in ("pages/contact.html", "enquiries/partials/sportello_form.html", "enquiries/contact.html"):
        source = (ROOT / "templates" / name).read_text(encoding="utf-8")
        assert not re.search(r"\d{3}[\s.]?\d{3}[\s.]?\d{3}", source), name
        assert "wa.me" not in source and "tel:" not in source, name
    # gate G2 closed: no form — the notice stands in the form's own seat, said before any click
    seat = main.select_one(".sportello__modulo#formulaire")
    assert seat.select_one('[data-gate="forms-closed"]') is not None
    assert main.select("form, input, textarea") == []


@pytest.mark.django_db
def test_with_the_forms_open_the_desk_holds_the_enquiries_form_and_its_one_primary(client, seeded, legal_published):
    main = _main(client.get("/fr/contact/").content.decode("utf-8"))
    assert main.select_one('[data-gate="forms-closed"]') is None
    forms = main.select("form")
    assert len(forms) == 1
    form = forms[0]
    assert form["method"] == "post" and form["action"] == "/fr/contact/formulaire/"
    assert form.select_one('input[name="csrfmiddlewaretoken"]') is not None
    trap = form.select_one('.hp-field[aria-hidden="true"] input[name="website_url"]')
    assert trap is not None
    names = {field["name"] for field in form.select("input[name], textarea[name], select[name]")}
    assert {"name", "email", "subject", "message", "consent"} <= names, names
    assert form.select_one('.form__privacy-link a[href="/fr/privacy-policy/"]') is not None
    primaries = main.select(".btn--primary")
    assert len(primaries) == 1 and primaries[0].name == "button" and primaries[0]["type"] == "submit"
    assert primaries[0].find_parent("form") is form


@pytest.mark.django_db
@pytest.mark.parametrize("lang", ["fr", "it", "en", "ar"])
def test_the_fraud_statement_is_its_own_sentences_in_one_amber_panel(get, lang):
    main = _main(get(f"/{lang}/attention-aux-fraudes/"))
    panel = main.select_one(
        'header.avvertenza-testa > .avvertenza[role="note"][aria-labelledby="antifraud-inset-title"]'
    )
    assert panel is not None and panel.select_one("h2#antifraud-inset-title") is not None
    texts = panel.select('[data-locked="p3.antifraud.body"]')
    assert len(texts) == 1
    body, _effective = locked_content.get("p3.antifraud.body", lang)
    assert texts[0].get_text() == body, "the words and their order unchanged"
    parts = texts[0].find_all(recursive=False)
    assert len(parts) >= 2 and all(p.name == "span" and "ls" in p["class"] for p in parts)
    assert "".join(p.get_text() for p in parts) == body
    # never restated in team words: the statement said once, its panel holding no list —
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026
    # (P1-2 of the integration review: the page showed less than the home's teaser of it): the page's one list of
    # signs is the home band's, carried whole beside the panel — its label, its five catalogue labels and their
    # symbols, in order, the same msgids (read from the frozen home partial, never retyped here)
    assert main.select(".frodi-segnali, .avvertenza li") == []
    assert main.get_text().count(parts[0].get_text().strip()) == 1
    home = (ROOT / "templates" / "pages" / "home" / "_antifraud.html").read_text(encoding="utf-8")
    rows = re.findall(r'<li>\{% svg_icon "([a-z-]+)" "icon" %\}\{% translate "([^"]+)" %\}</li>', home)
    label = re.search(r'class="allerta__etichetta t-label">\{% translate "([^"]+)" %\}<', home).group(1)
    signs = main.select("header.avvertenza-testa > .avvertenza-segnali")
    assert len(rows) == 5 and len(signs) == 1 and len(main.select(".avvertenza-segnali, .allerta__chips")) == 1
    with translation.override(lang):
        assert signs[0].select_one("h2.avvertenza-segnali__etichetta.t-label").get_text(strip=True) == gettext(label)
        drawn = [
            (li.select_one("svg.icon use")["href"].rsplit("#icon-", 1)[1], li.get_text(strip=True))
            for li in signs[0].select('ul.avvertenza-segnali__chips[role="list"] > li')
        ]
        assert drawn == [(symbol, gettext(msgid)) for symbol, msgid in rows]


@pytest.mark.django_db
def test_the_network_explorer_is_a_tablist_on_complete_markup_and_draws_no_ring(get):
    main = _main(get("/fr/reseau/"))
    explorer = main.select_one('section.rete-esplora[data-sec-js~="mappa"][data-label]')
    tabs = explorer.select("ul.mappa__nodi.mappa__anello > li > a.mappa__tasto")
    assert [a["href"] for a in tabs] == [
        "#rete-persons",
        "#rete-companies",
        "#rete-institutions",
        "#rete-universities",
        "#rete-professionals",
    ]
    for tab in tabs:
        panel = explorer.select_one(tab["href"])
        assert panel is not None and panel.name == "section" and panel.select_one("h3").get_text().strip()
        assert tab.get_text().strip() == panel.select_one("h3").get_text().strip()
    # relations are said, not drawn: no spoke, no ring drawing, no flag, no seal
    assert main.select(".mappa__raggio, .intesa, .sigillo, [data-sec='intesa']") == []
    assert all("icon" in svg.get("class", []) for svg in main.select("svg"))


@pytest.mark.django_db
def test_the_faq_guide_holds_the_search_the_themes_and_the_one_way_to_a_person(get):
    main = _main(get("/fr/faq/"))
    guide = main.select_one(".faq-banco__griglia > aside.faq-guida")
    assert guide.select_one('form input#faq-q[type="search"]') is not None
    themes = guide.select(".faq-temi button.faq-tema[data-cerca-tema]")
    assert len(themes) >= 2
    assert [a["href"] for a in guide.select(".faq-aiuto a")] == ["/fr/contact/"]
    assert main.select('.faq-rimando a[href="/fr/contact/"], [data-cerca-vuoto] a[href="/fr/contact/"]') == []


@pytest.mark.django_db
def test_the_public_forum_has_its_own_sheet_and_a_spy_over_its_sections(get):
    html = get("/fr/forum/")
    assert "css/dist/forum/pubblico.css" in html and "css/dist/forum/forum.css" not in html
    main = _main(html)
    nav = main.select_one('nav.forum-localnav[data-sec-js~="spia"]')
    links = [a["href"] for a in nav.select("a")]
    assert links and all(href.startswith("#") and main.select_one(href) is not None for href in links)
    assert main.select(".forum-hero .sigillo, .forum-hero svg:not(.icon)") == []
