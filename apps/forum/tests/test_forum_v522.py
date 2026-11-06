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
"""

from __future__ import annotations

import re

import pytest
from bs4 import BeautifulSoup

from cms import locked_content
from core import icons

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
    seals = [seal["data-mark"] for seal in main.select("span.sigillo[data-mark]")]
    assert seals == [icons.MARKS["forum"].id]
    assert main.select_one(".forum-hero__disegno span.sigillo") is not None
    # the hub and the faint drawing behind the actions draw the mark itself, decorative
    for drawing in main.select(".forum-anello__centro, .forum-azioni__fondale"):
        assert drawing["aria-hidden"] == "true" and drawing.select_one("svg.sigillo__mark[data-mark='ile-forum']")


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
    arrival = stations[-1]
    assert "forum-obiettivi__tappa--arrivo" in arrival["class"]
    assert arrival.select_one(f"use[href$='#icon-{icons.MARKS['forum'].id}']") is not None


@pytest.mark.parametrize("lang", ["fr", "ar"])
def test_the_nine_actors_are_one_register_with_the_four_audiences_glyphs(client, event, lang):
    main = _main(client, lang)
    sentence = main.select_one('p[data-locked="p2.forum.audience.body"][data-registro]')
    assert sentence is not None and sentence.select("a") == []
    actors = sentence.select("span.forum-attore")
    assert len(actors) == 9
    glyphs = {
        int(re.search(r"forum-attore--(\d+)", " ".join(actor["class"])).group(1)): use["href"].rsplit("#icon-", 1)[1]
        for actor in actors
        if (use := actor.select_one(".sez-disc use"))
    }
    expected = {
        1: icons.concept("audience", "institution"),
        2: icons.concept("audience", "company"),
        5: icons.concept("audience", "university"),
        6: icons.concept("actor", "training_body"),
    }
    assert glyphs == expected
    assert sorted(set(expected.values())) == ["building", "institution", "presentation", "university"]


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
