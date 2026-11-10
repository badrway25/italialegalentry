"""
The chapter marks of the public site, read in the rendered pages — V5.12 §7 (W1, lane B), and V5.22 (lane S).

Until V5.12 every section head of the public site drew `ile-steps`, the journey's stair, whatever its title said:
«Par e-mail», «Documentation», «Autorités», the Forum's programme, an FAQ group (83 times on 35 pages, LANE_B §1.1).
V5.12 made each head draw the glyph of its section's concept, or nothing.

V5.22 (SECTION_SYSTEM_V2 §0 item 3, §4.1 rule 1, §4.10 — the owner's V5.22 §6: «the current tiny icons placed above
headings are not visually strong enough», an approved owner/product decision): the bare 24 px mark above a title is
retired everywhere. A head now draws its concept as a T1 seal integrated in its composition (the head folio's small
arch seat, components/sezioni/sigillo.html), or not at all; never `ile-steps`; never two concepts in one head (V5.20
strict rule: the old expectation — a concept glyph above the title — conflicts with the decision; the invariants it
protected, no stair and one concept a head, hold, and «no glyph above a title» is added).

V5.22 lane H (SECTION_SYSTEM_V2 §3.1, §4.1 rule 1, §4.10; the home's composition V2, label v522-h-final-improve): the
home's exception goes. Lane H recomposed every home section on the library, so the home draws no bare chapter mark any
more and is held to the rule every other page holds — no stair, no bare mark, no glyph above a title, each seal once —
and, in place of V5.12's two chapter marks (compass, signpost), the three seals §3.1 places on it: the orientation's
origin (`ile-orienta`, S2), «la protezione»'s shield (`ile-scudo`, S6) and the reserved row's key (`ile-accesso`, S8),
each exactly once, on the French and the Arabic home (V5.20 strict rule: the old expectation — the home's chapter marks —
conflicts with the approved V5.22 decision; the invariant is stronger, the home loses its exemption and gains an exact
set of seals).
"""

from __future__ import annotations

import re

import pytest

from core import icons

pytestmark = pytest.mark.django_db

PAGES = [
    "/fr/",
    "/ar/",
    "/fr/contact/",
    "/fr/contact/formulaire/",
    "/fr/faq/",
    "/fr/parcours/",
    "/fr/parcours/salaried_work/",
    "/ar/parcours/salaried_work/",
    "/fr/diplomes-et-titres/",
    "/fr/formation/",
    "/fr/orientation/",
    "/fr/entreprises/",
    "/fr/entreprises/recueil-des-besoins/",
    "/fr/institutions/",
    "/fr/universites-et-formation/",
    "/fr/collaboration/institutions/",
    "/fr/collaboration/universites-formation/",
    "/fr/projet-pilote/",
    "/fr/forum/",
    "/fr/le-projet/",
    "/fr/agami/",
    "/fr/reseau/",
    "/fr/attention-aux-fraudes/",
    "/fr/actualites/",
    "/fr/glossaire/",
    "/fr/partenaires/",
]
#: FINAL MICRO-PASS §2.1, §5 A3 (V5.20 strict rule: the head folios' T1 seals left with the eyebrow's tile — «not an
#: architecture website»): the eight folios that drew their page's seal are typographic, as the four below always were
FORMER_SEALS = (
    "/fr/parcours/",
    "/fr/parcours/salaried_work/",
    "/ar/parcours/salaried_work/",
    "/fr/formation/",
    "/fr/entreprises/",
    "/fr/institutions/",
    "/fr/universites-et-formation/",
    "/fr/attention-aux-fraudes/",
)
#: the home, recomposed by lane H (SECTION_SYSTEM_V2 §3.1), is no longer exempt: it draws no bare mark, and its seals
#: are exactly the three §3.1 places on it, each once — the orientation's origin, «la protezione»'s shield, the
#: reserved row's key (V5.20 strict rule; the exemption V5.12 and lane S kept «until lane H recomposes it» goes)
#: FINAL MICRO-PASS §5 A1/A3 (V5.20 strict rule): the orientation's origin seal and «la protezione»'s seated shield
#: left (the shield is drawn bare, no seal) — the home's one seal is the reserved door's key, its arch a brand signature
#: the owner kept, once
HOME_SEALS = {"/fr/": ["ile-accesso"], "/ar/": ["ile-accesso"]}
#: the head folios whose concept has no ILE mark: typographic (a Lucide disc in the folio's seat was the old device) —
#: and, FINAL MICRO-PASS §5 A3, every other head folio
TYPOGRAPHIC = ("/fr/contact/", "/fr/reseau/", "/fr/diplomes-et-titres/", "/fr/agami/", *FORMER_SEALS)
MARK = re.compile(r'<svg class="icon chapter__mark[^"]*"[^>]*><use href="[^"#]*#icon-([a-z0-9-]+)"')
SEAL = re.compile(r'<span class="sigillo [^"]*" data-mark="([a-z-]+)"')
HEAD = re.compile(r'<div class="(?:section__header )?chapter__head">(.*?)<h2', re.S)


def _main(html: str) -> str:
    return html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]


@pytest.fixture
def pages(client, seeded, phase3_open, legal_published):
    found = {}
    for path in PAGES:
        response = client.get(path)
        if response.status_code == 404:  # a surface its gate keeps closed (V5.12 §13) has no head to read
            continue
        assert response.status_code == 200, (path, response.status_code)
        found[path] = response.content.decode("utf-8")
    return found


def test_no_public_page_draws_the_stair_nor_a_glyph_above_a_title_and_each_folio_says_its_concept_once(pages):
    assert len(pages) >= 18, sorted(set(PAGES) - set(pages))
    for path, html in pages.items():
        main = _main(html)
        assert "#icon-ile-steps" not in main, path
        # the premium forms' glyph tiles (V5.15 W3, preserved by V5.22 §9.8) hold their concept inside a container
        bare = re.sub(r'<span class="glyph-tile[^"]*"[^>]*>.*?</span>', "", main, flags=re.S)
        assert not MARK.findall(bare), (path, "a bare mark above a title (retired, V5.22 §0 item 3)")
        for before_title in HEAD.findall(main):
            assert "<svg" not in before_title, (path, "a glyph stacked above a chapter title")
        seals = SEAL.findall(main)
        assert len(seals) == len(set(seals)), (path, "one concept, said once a page by its seal", seals)
        assert set(seals) <= {mark.id for mark in icons.MARKS.values()}, (path, seals)
        if path in HOME_SEALS:
            assert seals == HOME_SEALS[path], (path, "the home's one seal, once", seals)
        if path in FORMER_SEALS:
            assert not seals, (path, "no seal on the page any more", seals)
        if path in TYPOGRAPHIC:
            folio = main.split('class="ingresso__label"', 1)[1].split("</p>", 1)[0]
            assert "<svg" not in folio and "sigillo" not in folio, (path, "a typographic folio")
            assert re.sub(r"<[^>]+>", "", folio.split(">", 1)[1]).strip(), (path, "the folio's words")


def test_the_stair_still_says_my_journey_in_the_console(client, seeded, person_user):
    """The other half of the rule: the one seat the stair keeps — «Mon parcours» in a person's rail."""
    client.force_login(person_user)
    response = client.get("/fr/espace-reserve/", follow=True)
    assert response.status_code == 200
    html = response.content.decode("utf-8")
    assert "#icon-ile-steps" in html, "the rail's «Mon parcours»"
