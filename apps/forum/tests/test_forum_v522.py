"""
V5.22 — the Forum's V2 composition (SECTION_SYSTEM_V2 §3.16; lane P2, label v522-p2-build), rendered by the server:

* FO0: the page's one T1 seal, `ile-forum`, drawn in the head (a page says its concept once by its seal: the hub of the
  audience's ring and the actions' faint drawing are the mark's drawing, never a second seal);
* FO1: «QUI SOMMES-NOUS» and «POURQUOI…» each one locked paragraph, cut at render — the opening clause, the last
  sentence set in place as the statement — their text the registry's, whole, once;
* FO2a: the objectives' one locked sentence cut on its own « ; » into eight stations, in order, its punctuation kept;
  the arrival station carries the Forum's T2 mark;
* FO2b: the nine actors of the locked sentence, its own spans, one register: the four that name an ILE audience carry
  the registry's glyph (`institution`, `building`, `university`, `presentation`), the five others none; no link inside;
* FO3: two action plates on stone, the locked labels as their links, the help line at their foot.

RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D): FO0's
seal, FO2a's arrival mark and FO2b's ring of nine spans left the public page (no geometry as filler) — the page draws
no seal, the objectives are their clauses, the audience its locked sentence whole; FO1 and FO3 are unchanged.
"""

from __future__ import annotations

import pytest
from bs4 import BeautifulSoup

from cms import locked_content

pytestmark = pytest.mark.django_db


def _main(client, lang="fr") -> BeautifulSoup:
    response = client.get(f"/{lang}/forum/")
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    return BeautifulSoup(html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0], "html.parser")


def _locked(main: BeautifulSoup, key: str) -> list[str]:
    return [el.get_text() for el in main.select(f'[data-locked="{key}"]')]


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_forum_says_its_concept_once_by_its_seal(client, event, lang):
    main = _main(client, lang)
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D;
    # the brief's «no geometry as filler: arches, arcs, curves, nodes»): the page says its concept by its words — the
    # hemicycle seal left the head, and with it the ring's hub and the actions' faint drawing: no seal, no mark drawing,
    # no second one anywhere (the old «at most once» held at zero); the head keeps its h1 and its fact sheet
    assert main.select("span.sigillo, [data-mark], svg.sigillo__mark") == []
    assert main.select(".forum-hero__disegno, .forum-anello, .forum-anello__centro, .forum-azioni__fondale") == []
    head = main.select_one("header.forum-hero#forum-top")
    assert len(main.find_all("h1")) == 1 and head.find("h1") is not None
    assert head.select_one(".forum-hero__scheda .forum-hero__meta") is not None


def test_the_pair_and_the_objectives_keep_their_prescribed_texts(client, event):
    main = _main(client)
    for key in ("who.body", "why.body", "objectives.body", "audience.body"):
        assert _locked(main, f"p2.forum.{key}") == [locked_content.text(f"p2.forum.{key}", "fr")], key
    who = main.select_one('[data-locked="p2.forum.who.body"]')
    assert who.find("span", class_="ls-1").get_text().rstrip().endswith(",")  # the opening clause, to its first comma
    why = main.select_one('[data-locked="p2.forum.why.body"]')
    assert why.find_all("span", recursive=False)[-1]["class"] == ["ls", "ls-3"]  # the statement, set in place
    stations = main.select('ol.forum-obiettivi[data-locked="p2.forum.objectives.body"] > li')
    assert len(stations) == 8
    assert "".join(li.get_text() for li in stations) == locked_content.text("p2.forum.objectives.body", "fr")
    assert all(li.get_text().rstrip().endswith(";") for li in stations[:-1])
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D):
    # the objectives are a plain list of their clauses — the arrival station's mark left with the stations' line: no
    # clause draws a glyph, every row is the same kind of row
    assert all(li["class"] == ["forum-obiettivi__tappa"] and li.select("svg, use") == [] for li in stations)


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_nine_actors_are_one_register_with_the_four_audiences_glyphs(client, event, lang):
    main = _main(client, lang)
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026 (lane D;
    # replaces «the nine actors are one register with the four audiences' glyphs»): the audience is the locked sentence
    # WHOLE, read as the band's statement — the ring that cut it into nine floating words, their discs and their
    # commas left (a sentence is read, not orbited). The sentence stays the registry's text, once, with no link and no
    # span or glyph inside; the nine actors are still said, in order, by its own words
    sentence = main.select_one('p.forum-uditorio__frase[data-locked="p2.forum.audience.body"]')
    assert sentence is not None and sentence.select("a") == [] and sentence.find_all() == []
    assert len(main.select('[data-locked="p2.forum.audience.body"]')) == 1  # whole and once (its words: the test above)
    assert main.select("span.forum-attore, .forum-uditorio .sez-disc, svg.forum-anello__raggi") == []
    assert main.select_one('section.forum-uditorio[data-ground="paper"]') is not None


def test_the_actions_are_two_plates_with_their_prescribed_labels(client, event):
    main = _main(client)
    plates = main.select(".forum-azioni ul > li.forum-azioni__lastra.sez-plate")
    assert [plate["data-audience"] for plate in plates] == ["company", "institution"]
    labels = [plate.select_one(".forum-azioni__link").get_text(strip=True) for plate in plates]
    assert labels == [
        locked_content.text("p2.forum.registration.button_secondary_pilot", "fr"),
        locked_content.text("p2.forum.registration.button_secondary_collab", "fr"),
    ]
    assert [plate.select_one(".sez-disc use")["href"].rsplit("#icon-", 1)[1] for plate in plates] == [
        "building",
        "institution",
    ]
