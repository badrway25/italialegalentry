"""Homepage: composition, gates, prescribed texts, accessibility outline — in both gate states."""

from __future__ import annotations

import datetime as dt
import re

import pytest
from freezegun import freeze_time

from cms import locked_content
from cms.forbidden import scan
from cms.models import PublicationStatus
from core import flags
from pages.models import HomeSection, HomeSectionTranslation, SectionKey
from pages.tests.conftest import LANGS, PHASE3_HOME_KEYS, escaped, section_order, text_of


def h1_text(html: str) -> str:
    """The H1's text, tags stripped, whitespace collapsed: the hero sets its title in masked lines
    (one <span> per line, the trademark sign apart) and the choreography must not change a
    character of the locked string."""
    inner = re.search(r"<h1[^>]*>(.*?)</h1>", html, flags=re.S).group(1)
    return " ".join(re.sub(r"<[^>]+>", "", inner).split()).replace(" ™", "™")


pytestmark = pytest.mark.django_db

# The gate-closed composition of the run-up to the Forum: the banner sits under the hero until
# 2 Oct 2026, 00:00 Rome. A test comparing a page with it freezes the clock there
# (``before_the_forum``) — on the real clock the banner is gone and the comparison fails.
CLOSED_ORDER = ["hero", "banner", "entrances", "orientation", "pathways", "trust", "ecosystem"]
OPEN_ORDER = [
    "hero",
    "entrances",
    "orientation",
    "pathways",
    "pilot",
    "trust",
    "antifraud",
    "ecosystem",
    "reserved",
]  # no news chapter while no article is live (the review fix, m4): the tests that need it publish one


# ---------------------------------------------------------------------------------------------
# Rendering in the four languages, both gate states
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("lang", LANGS)
def test_home_renders_in_every_language_gate_closed(before_the_forum, page, seeded, lang):
    response, html = page(f"/{lang}/")
    assert response.status_code == 200
    assert html.count("<h1") == 1
    assert f'<html lang="{lang}"' in html
    assert section_order(html) == CLOSED_ORDER


@pytest.mark.parametrize("lang", LANGS)
def test_home_renders_in_every_language_phase3_open(page, seeded, phase3_open, lang):
    response, html = page(f"/{lang}/")
    assert response.status_code == 200
    assert html.count("<h1") == 1
    assert section_order(html) == OPEN_ORDER  # the Forum banner expired on 2 Oct 2026


def test_arabic_home_is_rtl_and_marks_french_fallback(page, seeded, phase3_open):
    _response, html = page("/ar/")
    assert '<html lang="ar" dir="rtl"' in html
    assert " is-rtl" in html
    # Prescribed texts have no official Arabic version: French, explicitly tagged — in the V5 hero the h1 holds the
    # name (visually hidden) and the promise, each a locked text in its own span. The promise carries the fallback
    # marker; the name is an English name on every page and says so, as the header's lock-up does (a11y F10).
    assert re.search(r'<span class="visually-hidden he__name" id="hero-name" translate="no" dir="ltr" lang="en">', html)
    assert '<span class="he__promise" lang="fr" dir="ltr">' in html
    assert 'class="gradino__body" lang="fr"' in html


def test_french_home_has_no_fallback_lang_attributes_on_locked_texts(page, seeded, phase3_open):
    _response, html = page("/fr/")
    # the name's own language is not a fallback marker: «Italy Legal Entry» is English on the French page too
    assert re.search(r'<span class="visually-hidden he__name" id="hero-name" translate="no" dir="ltr" lang="en">', html)
    assert not re.search(r'<h1 class="he__title"[^>]* lang="', html)
    assert '<span class="he__promise">' in html
    assert 'class="gradino__body">' in html


def test_heading_outline_is_logical(page, seeded, phase3_open):
    _response, html = page("/fr/")
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    levels = [int(n) for n in re.findall(r"<h([1-6])\b", main)]
    assert levels[0] == 1 and levels.count(1) == 1
    for previous, current in zip(levels, levels[1:]):
        assert current <= previous + 1, f"heading level jumps from h{previous} to h{current}"


def test_home_has_no_inline_style_or_external_resource(page, seeded, phase3_open):
    _response, html = page("/fr/")
    assert not re.search(r"<[a-z][^>]*\sstyle=", html)
    assert not re.search(r"\son[a-z]+=\"", html)
    urls = re.findall(r'(?:src|href|srcset|content|action)="(https?://[^"]+)"', html)
    assert [u for u in urls if "testserver" not in u] == []
    assert 'href="/static/css/dist/pages/css/pages.css"' in html
    assert 'href="/static/css/dist/pages/css/hero.css"' in html
    # The home's one script (V5.4 plan §2.3): the hero's module and the dismissible notice, bundled by esbuild.
    assert '<script type="module" src="/static/js/dist/home.js"></script>' in html
    assert "/static/pages/js/home.js" not in html


# ---------------------------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------------------------
def test_interim_hero_before_phase3(page, seeded):
    _response, html = page("/fr/")
    assert 'data-hero-variant="interim"' in html
    assert h1_text(html) == "Un écosystème pour les parcours réguliers vers l’Italie"
    assert "Orientation · Formation · Mobilité régulière" in html
    # Body = Phase 1 prescribed fragment, resolved through the registry.
    assert escaped(text_of("p1.persons.replacement_1")) in html
    assert 'href="/fr/orientation/"' in html
    assert 'href="/fr/entreprises/recueil-des-besoins/"' in html


def test_phase3_hero_renders_exact_prescribed_texts(page, seeded, phase3_open):
    _response, html = page("/fr/")
    assert 'data-hero-variant="phase3"' in html
    hero = html.split('data-section="hero"', 1)[1].split("</section>", 1)[0]
    # The V5 hero's one h1: the locked name (visually hidden, for assistive technology and search) and the locked
    # promise in sight — each whole, character for character (HERO_FINAL.md §2.1; plan §1.17 «one brand expression»).
    name = re.search(r'<span class="visually-hidden he__name"[^>]*>(.*?)</span>', hero, flags=re.S).group(1)
    promise = re.search(r'<span class="he__promise"[^>]*>(.*?)</span>', hero, flags=re.S).group(1)
    assert name.strip() == escaped(text_of("p3.hero.title"))
    assert promise.strip() == escaped(text_of("p3.hero.subtitle"))
    assert h1_text(hero) == f"{text_of('p3.hero.title')} {text_of('p3.hero.subtitle')}"
    assert escaped(text_of("p3.hero.body")) in hero
    assert "Un écosystème pour les parcours réguliers" not in hero
    # The path's stations: the shore, then the pilot sequence's second to sixth steps — whole, in their prescribed
    # order.
    sequence = locked_content.LOCKED_TEXTS["fr"]["p3.pilot.sequence"]
    labels = re.findall(r'<span class="he-station__label"[^>]*>(.*?)</span>', hero, flags=re.S)
    assert labels == ["Maroc", *(escaped(step) for step in sequence[1:6])]
    assert hero.count("data-station=") == 6
    assert escaped(sequence[0]) not in hero and escaped(sequence[6]) not in hero


def test_date_alone_does_not_switch_the_hero(page, seeded, set_flag):
    set_flag("phase3_public", False, enabled_from=dt.datetime(2026, 10, 2, tzinfo=dt.UTC))
    with freeze_time("2026-10-10 12:00:00"):
        flags.invalidate()
        _response, html = page("/fr/")
    assert 'data-hero-variant="interim"' in html
    assert escaped(text_of("p3.hero.subtitle")) not in html


def test_no_figure_ships_without_its_caption(page, seeded):
    """
    Art direction A §6.2: a <figure> without a <figcaption> is a defect, and the caption must carry
    place, date, one factual sentence and a credit.

    This is the rule that makes anonymous stock photography structurally impossible rather than
    merely discouraged. The library inherited from the previous build does not pass it — six
    interchangeable frames served fifty-two pages, none captioned, none credited — so the home plate
    carries the page on type alone until a curated image exists. That is not a fallback: the
    direction requires the site to be recognisable with no photographs at all.
    """
    _response, html = page("/fr/")
    figures = html.count("<figure")
    captions = html.count("<figcaption")
    assert figures == captions, f"{figures} <figure> for {captions} <figcaption>"


def test_the_hero_carries_the_owners_doorway_and_no_uncaptioned_figure(page, seeded):
    """Since 23/09/2026 the arch, the key and the steps of legalitalentry.it are the project's own
    composition (BRAND_ASSETS.md §2): the photograph lives INSIDE the arch, as the owner's site has
    it, and is the only image of the hero. It is not a <figure>: nothing to caption."""
    _response, html = page("/fr/")
    hero = html.split('data-section="hero"', 1)[1].split("</section>", 1)[0]
    # The V5 stage (W2-D): the photograph is a <picture> of the door-master derivatives in stage units — the LCP
    # element, the one high-priority image —, the arch, the inner door and the steps stay the SVG, the key is an HTML
    # layer that turns once; no <image> element is left.
    assert 'class="door-stage__photo"' in hero and 'class="door-stage__key doorway__key"' in hero
    assert 'class="doorway__steps"' in hero and 'class="doorway__arch"' in hero and 'class="doorway__inner"' in hero
    assert "<figure" not in hero
    assert hero.count("<image ") == 0
    assert hero.count('fetchpriority="high"') == 1, "the door's photograph, nothing else"
    assert hero.count("<picture") == 9, "the door and the four origins' two layers (black-and-white, colour)"
    assert hero.count('loading="lazy"') == 8, "every photograph but the door is lazy"
    assert "doorway-arch-576.webp" in hero and "doorway-arch-1200.avif" in hero


def test_the_four_photographs_pair_with_the_four_entrances_in_order(page, seeded):
    """The template pairs the photographs with the entrances BY ORDER ({% cycle %}): the order of
    pages.content.ENTRANCES is the pairing, and this test is what holds it (PROVENANCE.json names the audiences)."""
    _response, html = page("/fr/")
    hero = html.split('data-section="hero"', 1)[1].split("</section>", 1)[0]
    pairs = re.findall(r'data-aud="([a-z]+)" data-photo="([a-z-]+)"', hero)
    assert pairs == [
        ("person", "lectrice-bibliotheque-dos"),
        ("company", "chai-cuve-chene"),
        ("institution", "table-en-seance"),
        ("university", "paillasse-deux-etudiantes"),
    ]
    for _actor, slug in pairs:
        # src and srcset, in the black-and-white layer and in the colour layer
        assert hero.count(f"he-{slug}-1x1-192.webp") == 4, slug


def test_the_doors_preload_and_sources_are_character_identical(page, seeded):
    """CD C-9: the preload (home.html) and the hero's AVIF <source> carry the same candidates and the same sizes, so the
    preloaded file is the one the browser then picks."""
    _response, html = page("/fr/")
    preload = re.search(
        r'<link rel="preload" as="image" type="image/avif" fetchpriority="high" imagesrcset="([^"]+)" '
        r'imagesizes="([^"]+)">',
        html,
    )
    assert preload, "the door's preload"
    source = re.search(r'<source type="image/avif" srcset="([^"]+doorway-arch[^"]+)" sizes="([^"]+)">', html)
    assert source, "the door's AVIF source"
    assert preload.group(1) == source.group(1) and preload.group(2) == source.group(2)
    webp = re.search(r'<source type="image/webp" srcset="([^"]+doorway-arch[^"]+)" sizes="([^"]+)">', html)
    assert webp and webp.group(2) == source.group(2)


def _aria_hidden_ancestors_of(html: str, needle: str) -> list[str]:
    """The open elements carrying aria-hidden="true" around the first element whose start tag contains ``needle``."""
    from html.parser import HTMLParser

    void = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}

    class Walker(HTMLParser):
        def __init__(self):
            super().__init__()
            self.stack: list[tuple[str, bool]] = []
            self.found: list[str] | None = None

        def handle_starttag(self, tag, attrs):
            hidden = dict(attrs).get("aria-hidden") == "true"
            text = self.get_starttag_text() or ""
            if self.found is None and needle in text:
                self.found = [t for t, h in self.stack if h]
            if tag not in void:
                self.stack.append((tag, hidden))

        def handle_endtag(self, tag):
            for i in range(len(self.stack) - 1, -1, -1):
                if self.stack[i][0] == tag:
                    del self.stack[i:]
                    break

    walker = Walker()
    walker.feed(html)
    assert walker.found is not None, needle
    return walker.found


@pytest.mark.parametrize(
    "lang, label",
    [("fr", "Rejouer l’animation de la porte"), ("ar", "إعادة تشغيل الرسوم المتحركة للباب")],
)
def test_the_niche_is_decorative_and_its_one_control_is_the_replay_button(page, seeded, lang, label):
    """The review fix (design V5.4, W2-D, 9 October 2026): keyboard users get the repeatable flow too. The door stage
    stays decorative (aria-hidden on the stage, the reveal and the halo — not on the niche), and beside the stage, in
    the door box, stands the one control of the niche: a real button over the golden key, named by the catalogue in
    the page's language, outside every aria-hidden subtree (a focusable control inside one would be unreachable for
    assistive technology). hero.js shows it only on a page that moves; hero.css hides it under reduced motion and
    forced colours."""
    _response, html = page(f"/{lang}/")
    hero = html.split('data-section="hero"', 1)[1].split("</section>", 1)[0]
    assert '<div class="he-niche" data-niche>' in hero, "the niche itself is not aria-hidden: it holds a control"
    assert '<div class="door-stage he-door" data-door aria-hidden="true">' in hero
    assert '<span class="he-niche__reveal" aria-hidden="true">' in hero
    assert 'class="he-niche__halo" aria-hidden="true"' in hero
    button = f'<button type="button" class="he-replay" data-replay aria-label="{label}"></button>'
    assert hero.count(button) == 1, "one replay control, named in the page's language"
    assert hero.count("<button") == 1
    assert _aria_hidden_ancestors_of(hero, 'class="he-replay"') == []
    # the key's light response: its halo behind the key and the glint inside the key, both decorative layers of the
    # stage
    assert 'class="kt__l he-key-halo" data-key-halo' in hero and 'class="kt__l kg__glint" data-key-glint' in hero
    assert _aria_hidden_ancestors_of(hero, "data-key-glint") == ["div"]


def test_interim_hero_draws_the_path_the_origins_and_the_door_without_a_station(page, seeded):
    """While gate G3 is closed the pilot sequence may not be shown: the path, the four origins and the door are drawn,
    the stations are not (test_no_phase3_prescribed_text_while_gate_closed holds the words)."""
    _response, html = page("/fr/")
    hero = html.split('data-section="hero"', 1)[1].split("</section>", 1)[0]
    assert 'data-hero-variant="interim"' in hero
    assert "data-station=" not in hero and "he-stations" not in hero
    assert hero.count("<picture") == 9 and 'class="door-stage__photo"' in hero
    assert hero.count('class="he-origin"') == 4
    assert 'class="he__eyebrow"' in hero


def test_hero_disabled_keeps_exactly_one_h1(page, seeded):
    HomeSection.objects.filter(key=SectionKey.HERO).update(is_enabled=False)
    _response, html = page("/fr/")
    assert 'data-section="hero"' not in html
    assert html.count("<h1") == 1
    assert '<h1 class="visually-hidden">' in html


# ---------------------------------------------------------------------------------------------
# Prescribed Phase 3 texts: absent when closed, present when open
# ---------------------------------------------------------------------------------------------
@pytest.mark.parametrize("lang", LANGS)
def test_no_phase3_prescribed_text_while_gate_closed(page, seeded, lang):
    _response, html = page(f"/{lang}/")
    for key in PHASE3_HOME_KEYS:
        assert escaped(text_of(key)) not in html, key
    assert text_of("p3.hero.title") not in html  # the upper-case prescribed title
    for entry in ("faq_visas", "faq_recruitment_agency", "faq_preassessment_guarantee", "faq_diplomas", "faq_who"):
        assert f'data-faq="{entry}"' not in html
    for step in ("PROFILS ET COMPÉTENCES", "PRÉPARATION AVANT LE DÉPART"):
        assert step not in html


def test_before_phase3_date_even_with_flag_enabled(page, seeded, before_phase3):
    _response, html = page("/fr/")
    assert 'data-hero-variant="interim"' in html
    assert escaped(text_of("p3.antifraud.body")) not in html
    assert 'data-section="pilot"' not in html


def test_phase3_prescribed_texts_present_when_open(page, seeded, phase3_open):
    _response, html = page("/fr/")
    for key in PHASE3_HOME_KEYS:
        assert escaped(text_of(key)) in html, key
    from cms import locked_content

    # The pilot sequence is on the page where the hero's path carries it (its second to sixth steps, after the
    # origin's shore): the chapters under the hero do not print it a second time (below: the model is said once).
    for step in locked_content.get("p3.pilot.sequence", "fr")[0][1:6]:
        assert escaped(step) in html
    for pathway in locked_content.get("p3.persons.pathways", "fr")[0]:
        assert escaped(pathway["title"]) in html
        assert escaped(pathway["description"]) in html
    faq = {item["key"]: item for item in locked_content.get("p3.faq.items", "fr")[0]}
    for key in ("faq_visas", "faq_recruitment_agency", "faq_preassessment_guarantee", "faq_diplomas", "faq_who"):
        assert escaped(faq[key]["answer"]) in html, key


@pytest.mark.parametrize("state", ["closed", "open"])
def test_forbidden_formulations_scan_is_clean(request, page, seeded, state):
    if state == "open":
        request.getfixturevalue("phase3_open")
    for lang in LANGS:
        _response, html = page(f"/{lang}/")
        assert scan(html) == [], (state, lang)
        assert "®" not in html
        assert "Italy Legal Entry™" in html
        emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", html))
        assert emails <= {"contact@agamieuromed.org"}


# ---------------------------------------------------------------------------------------------
# Four entrances — exactly four, in both states
# ---------------------------------------------------------------------------------------------
def _entrances(html: str) -> list[str]:
    block = html.split('<ol class="register register--entrances', 1)[1].split("</ol>", 1)[0]
    # since V2 the <li> carries its route: <li class="register__item" data-route="person">
    return block.split('<li class="register__item"')[1:]


def test_exactly_four_entrances_gate_closed(page, seeded):
    _response, html = page("/fr/")
    assert html.count('<ol class="register register--entrances') == 1
    items = _entrances(html)
    assert len(items) == 4
    titles = [re.search(r'class="entry__title"[^>]*>([^<]+)<', item).group(1) for item in items]
    assert titles == ["Personnes", "Entreprises", "Institutions", "Universités et organismes de formation"]
    targets = [re.search(r'class="entry" href="([^"]+)"', item).group(1) for item in items]
    assert targets == [
        "/fr/parcours/",
        "/fr/entreprises/recueil-des-besoins/",
        "/fr/collaboration/institutions/",
        "/fr/collaboration/universites-formation/",
    ]
    # The four line drawings are retired with the cards that carried them: "a section of identical
    # cards" and "every card containing an icon" at once, on the four most important links of the
    # site. Design V5.4 (W2-D step 3) retires what replaced them too: the four are never ranked, so no
    # ordinal 01–04, and no landform glyph nobody could decode — each row is its title, its sentence and
    # its call, with one arrow beside the call's words.
    assert not any("entrance-" in item and ".svg" in item for item in items)
    assert not any("entry__ordinal" in item or "route__glyph" in item for item in items)
    assert all(item.count("#icon-arrow") == 1 and 'class="entry__cta"' in item for item in items)


def test_exactly_four_entrances_phase3_open_with_prescribed_texts(page, seeded, phase3_open):
    _response, html = page("/fr/")
    items = _entrances(html)
    assert len(items) == 4
    for item, actor in zip(items, ("person", "company", "institution", "university")):
        assert escaped(text_of(f"p3.entrances.{actor}.title")) in item
        assert escaped(text_of(f"p3.entrances.{actor}.text")) in item
        assert escaped(text_of(f"p3.entrances.{actor}.button")) in item
        assert 'class="entry" href="/fr/' in item  # every entrance resolves to a page
    assert "/fr/parcours/" in items[0]


def test_entrances_are_h3_under_the_section_h2(page, seeded):
    _response, html = page("/fr/")
    assert '<h2 class="section__title" id="home-entrances-title">' in html
    assert html.count('<h3 class="entry__title"') == 4


# ---------------------------------------------------------------------------------------------
# Forum banner
# ---------------------------------------------------------------------------------------------
def test_forum_banner_present_before_2_october_under_the_hero(page, seeded):
    with freeze_time("2026-09-25 09:00:00"):
        flags.invalidate()
        _response, html = page("/fr/")
    assert 'data-banner="forum"' in html
    for key in ("p2.home.banner.title", "p2.home.banner.meta", "p2.home.banner.quote", "p2.home.banner.button"):
        assert escaped(text_of(key)) in html, key
    assert section_order(html)[:2] == ["hero", "banner"]
    assert 'href="/fr/forum/"' in html
    # Dismissal is client-side only: the control is inert markup until the script enables it.
    assert re.search(r'<button class="home-banner__dismiss" type="button" data-dismiss hidden>', html)


def test_forum_banner_absent_after_2_october(page, seeded):
    with freeze_time("2026-10-03 09:00:00"):
        flags.invalidate()
        _response, html = page("/fr/")
    assert 'data-banner="forum"' not in html
    assert 'data-section="banner"' not in html
    assert escaped(text_of("p2.home.banner.quote")) not in html
    # What the homepage is from then on, for as long as gate G3 stays closed.
    assert section_order(html) == [key for key in CLOSED_ORDER if key != "banner"]


def test_forum_banner_absent_when_flag_is_off(page, seeded, set_flag):
    set_flag("forum_banner", False)
    with freeze_time("2026-09-25 09:00:00"):
        flags.invalidate()
        _response, html = page("/fr/")
    assert 'data-section="banner"' not in html


def test_banner_sets_no_cookie(before_the_forum, client, seeded):
    # The banner is up only until 2 Oct 2026, 00:00 Rome: on the real clock this checked a homepage
    # without it. Frozen in the run-up to the Forum, and the banner is asserted to be on the page.
    response = client.get("/fr/")
    assert 'data-banner="forum"' in response.content.decode(), "the page under test carries the banner"
    assert set(response.cookies.keys()) <= {"csrftoken", "sessionid", "ile_language"}


# ---------------------------------------------------------------------------------------------
# Orientation, pathways, trust, anti-fraud
# ---------------------------------------------------------------------------------------------
def test_orientation_gate_closed_uses_neutral_stepper_and_disclaimer(page, seeded):
    _response, html = page("/fr/")
    block = html.split('data-section="orientation"', 1)[1].split("</section>", 1)[0]
    # the four neutral steps on the public passage «la linea» (W3-D: components/stepper.html), across from 48rem
    assert block.count('class="linea__step') == 4
    assert '<ol class="linea linea--across"' in block
    assert "aria-current" not in block and "linea__rank" not in block  # an explanation, not a progress state
    assert "pré-évaluation à caractère informatif" in block
    assert "autorités compétentes" in block
    assert 'href="/fr/orientation/"' in block


def test_orientation_phase3_uses_the_prescribed_sentence(page, seeded, phase3_open):
    _response, html = page("/fr/")
    block = html.split('data-section="orientation"', 1)[1].split("</section>", 1)[0]
    assert escaped(text_of("p3.persons.how_it_works")) in block
    assert 'class="linea' not in block and 'class="sequence' not in block


def test_pathways_gate_closed_shows_neutral_families_only(page, seeded):
    _response, html = page("/fr/")
    block = html.split('data-section="pathways"', 1)[1].split("</section>", 1)[0]
    assert block.count('class="register__item"') == 5
    assert 'class="pathway-list"' not in block
    assert 'href="/fr/parcours/"' in block
    from cms import locked_content

    for pathway in locked_content.get("p3.persons.pathways", "fr")[0]:
        assert escaped(pathway["description"]) not in html


def test_pathways_phase3_lists_the_eight_prescribed_pathways(page, seeded, phase3_open):
    _response, html = page("/fr/")
    block = html.split('data-section="pathways"', 1)[1].split("</section>", 1)[0]
    assert 'data-pathways="8"' in block
    assert block.count('class="pathway-list__item"') == 8


def test_trust_gate_closed_uses_phase1_fragments_and_neutral_statements(page, seeded):
    _response, html = page("/fr/")
    block = html.split('data-section="trust"', 1)[1].split("</section>", 1)[0]
    assert 'data-trust="interim"' in block
    # One thing once (pages.services._say_once): the hero's description IS the first of the two Phase 1 fragments,
    # so the chapter lists the other one and does not print the hero's sentence a second time.
    assert escaped(text_of("p1.persons.replacement_1")) not in block
    assert html.count(escaped(text_of("p1.persons.replacement_1"))) == 1
    assert escaped(text_of("p1.persons.replacement_2")) in block
    assert block.count('class="home-trust__column"') == 2
    assert 'href="/fr/avvertenze/"' in block


def test_trust_phase3_quotes_four_prescribed_faq_entries(page, seeded, phase3_open):
    _response, html = page("/fr/")
    block = html.split('data-section="trust"', 1)[1].split("</section>", 1)[0]
    assert re.findall(r'data-faq="([a-z_]+)"', block) == [
        "faq_visas",
        "faq_recruitment_agency",
        "faq_preassessment_guarantee",
        "faq_diplomas",
    ]


def test_antifraud_renders_nothing_while_gate_closed(page, seeded):
    _response, html = page("/fr/")
    main = html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]
    assert 'data-section="antifraud"' not in main
    assert "gradino" not in main and "antifraud-panel" not in main
    assert "fraude" not in main.lower()  # no substitute text is invented


def test_antifraud_callout_links_the_page_when_open(page, seeded, phase3_open):
    _response, html = page("/fr/")
    block = html.split('data-section="antifraud"', 1)[1].split("</section>", 1)[0]
    assert escaped(text_of("p3.antifraud.title")) in block
    assert escaped(text_of("p3.antifraud.body")) in block
    assert 'href="/fr/attention-aux-fraudes/"' in block
    # one sign for one warning: the registry's glyph of «Attention aux fraudes» (apps/core/icons.py), the one the
    # footer and the navigation's panels draw beside it — never the account-security shield
    assert block.count("#icon-shield-alert") == 1 and '#icon-shield"' not in block


def test_gate_cannot_be_bypassed_from_the_back_office(before_the_forum, page, seeded):
    """Clearing requires_gate on a Phase 3 section must not publish its prescribed texts."""
    HomeSection.objects.filter(key__in=["pilot", "antifraud", "reserved"]).update(requires_gate="")
    _response, html = page("/fr/")
    assert section_order(html) == CLOSED_ORDER
    assert escaped(text_of("p3.antifraud.body")) not in html


# ---------------------------------------------------------------------------------------------
# News
# ---------------------------------------------------------------------------------------------
def test_news_section_hidden_before_phase3_without_articles(page, seeded):
    _response, html = page("/fr/")
    assert 'data-section="news"' not in html


def test_news_section_appears_before_phase3_once_an_article_is_published(page, seeded, article_factory):
    article_factory("Programme du Forum publié")
    _response, html = page("/fr/")
    assert 'data-section="news"' in html
    assert "Programme du Forum publié" in html


def test_news_section_hidden_in_phase3_too_while_no_article_is_live(page, seeded, phase3_open):
    """The review fix (design V5.4, W2-D, m4): with gate G3 open the home announced an empty chapter — «Actualités»,
    then «Aucune actualité publiée pour le moment» — between the warning and the promoter. The chapter is on the home
    once an article is live, in either gate state; the news' own page keeps its empty state, which says which space
    is empty (DL54-33: the news' glyph, never the documents')."""
    _response, html = page("/fr/")
    assert 'data-section="news"' not in html
    assert "Aucune actualité publiée" not in html
    _response, index = page("/fr/actualites/")
    block = index.split('class="empty-state"', 1)[1].split("</div>", 1)[0]
    assert "#icon-newspaper" in block and "#icon-document" not in block and "#icon-empty" not in block


def test_news_section_appears_in_phase3_once_an_article_is_published(page, seeded, phase3_open, article_factory):
    article_factory("Programme du Forum publié")
    _response, html = page("/fr/")
    assert section_order(html) == [*OPEN_ORDER[:7], "news", *OPEN_ORDER[7:]]
    block = html.split('data-section="news"', 1)[1].split("</section>", 1)[0]
    assert "Programme du Forum publié" in block and 'class="empty-state"' not in block
    assert 'href="/fr/actualites/"' in block


def test_news_shows_only_live_articles_newest_first_max_three(page, seeded, phase3_open, article_factory):
    now = dt.datetime(2026, 10, 3, 9, 0, tzinfo=dt.UTC)
    for index, title in enumerate(["Article un", "Article deux", "Article trois", "Article quatre"]):
        article_factory(title, publish_at=now - dt.timedelta(days=10 - index))
    article_factory("Brouillon secret", status=PublicationStatus.DRAFT)
    article_factory("En relecture", status=PublicationStatus.REVIEW)
    article_factory("Archivé", status=PublicationStatus.ARCHIVED)
    article_factory("Programmé plus tard", status=PublicationStatus.SCHEDULED, publish_at=now + dt.timedelta(days=30))
    article_factory("Retiré", unpublish_at=now - dt.timedelta(days=1))
    _response, html = page("/fr/")
    block = html.split('data-section="news"', 1)[1].split("</section>", 1)[0]
    assert 'data-articles="3"' in block
    titles = re.findall(r'<h3 class="card__title"><a href="[^"]+">([^<]+)</a>', block)
    assert titles == ["Article quatre", "Article trois", "Article deux"]
    for hidden in ("Brouillon secret", "En relecture", "Archivé", "Programmé plus tard", "Retiré", "Article un"):
        assert hidden not in html


def test_news_translation_only_when_published(page, seeded, phase3_open, article_factory):
    from cms.models import TranslationStatus
    from news.models import ArticleTranslation

    article = article_factory("Titre français")
    ArticleTranslation.objects.create(
        master=article, language="it", title="Titolo in bozza", status=TranslationStatus.DRAFT
    )
    _response, html = page("/it/")
    assert "Titolo in bozza" not in html
    assert "Titre français" in html
    assert re.search(r'<article class="card card--link" lang="fr">', html)
    ArticleTranslation.objects.filter(master=article).update(
        status=TranslationStatus.PUBLISHED, title="Titolo italiano"
    )
    _response, html = page("/it/")
    assert "Titolo italiano" in html


# ---------------------------------------------------------------------------------------------
# Ecosystem, reserved area
# ---------------------------------------------------------------------------------------------
def test_ecosystem_shows_promoter_and_sober_empty_state(page, seeded):
    _response, html = page("/fr/")
    block = html.split('data-section="ecosystem"', 1)[1].split("</section>", 1)[0]
    assert "AGAMI — Dialogo Giuridico Interculturale APS" in block
    assert 'data-partners="0"' in block
    assert 'href="/fr/agami/"' in block and 'href="/fr/partenaires/"' in block
    assert "<img" not in block  # no logo, authorised or not, without a written authorisation


def test_ecosystem_lists_only_authorized_partners(page, seeded, partner_factory):
    partner_factory("Université partenaire autorisée")
    partner_factory("Organisme non autorisé", authorized=False)
    partner_factory("Partenaire en brouillon", status=PublicationStatus.DRAFT)
    _response, html = page("/fr/")
    assert "Université partenaire autorisée" in html
    assert "Organisme non autorisé" not in html
    assert "Partenaire en brouillon" not in html


def test_reserved_panel_needs_phase3_and_flag(page, seeded, set_flag, phase3_open):
    _response, html = page("/fr/")
    block = html.split('data-section="reserved"', 1)[1].split("</section>", 1)[0]
    for key in ("p3.reserved.title", "p3.reserved.body", "p3.reserved.button"):
        assert escaped(text_of(key)) in block
    assert 'href="/fr/compte/login/"' in block
    assert section_order(html)[-1] == "reserved"  # secondary: last, never protagonist
    # the row's sign is the key of the mark (the sprite's identity glyph), never a padlock
    assert block.count("#icon-ile-key") == 1 and "#icon-lock" not in block
    set_flag("reserved_area_public_link", False)
    _response, html = page("/fr/")
    assert 'data-section="reserved"' not in html
    assert escaped(text_of("p3.reserved.body")) not in html


def test_reserved_panel_links_dashboard_for_signed_in_visitor(client, seeded, phase3_open, person_user):
    client.force_login(person_user)
    html = client.get("/fr/").content.decode()
    block = html.split('data-section="reserved"', 1)[1].split("</section>", 1)[0]
    assert 'href="/fr/espace-reserve/"' in block


def test_reserved_panel_hidden_before_phase3(page, seeded):
    _response, html = page("/fr/")
    assert 'data-section="reserved"' not in html


# ---------------------------------------------------------------------------------------------
# The home around the hero (design V5.4, W2-D step 3): one thing once
# ---------------------------------------------------------------------------------------------
def _main(html: str) -> str:
    return html.split('<main id="main-content"', 1)[1].split("</main>", 1)[0]


def _under_the_hero(html: str) -> str:
    """The chapters: what the main landmark holds after the hero's own section."""
    return _main(html).split('data-section="hero"', 1)[1].split("</section>", 1)[1]


@pytest.mark.parametrize("lang", LANGS)
def test_the_morocco_italy_model_is_said_once_by_the_heros_path(page, seeded, phase3_open, lang):
    """
    The hero's path carries the model — the origin's shore, five stations of the pilot sequence, the door. The
    chapters under it do not draw it again: no second route between two shores in the pilot chapter (design V2's
    «voyage»), no jurisdiction bar from the country of origin to the Italian territory in the trust chapter.
    """
    _response, html = page(f"/{lang}/")
    main, below = _main(html), _under_the_hero(html)
    assert main.count('class="he-station__label"') == 6
    for gone in ('class="voyage', "data-voyage", 'class="jurisdiction', "data-share", 'class="timeline'):
        assert gone not in below, gone
    # No station of the hero's path is printed again under it: the pilot chapter is a statement — its prescribed
    # title, the section's sentence, one link — and the whole sequence stands on the pilot's own page.
    sequence = locked_content.LOCKED_TEXTS["fr"]["p3.pilot.sequence"]
    for step in sequence:
        assert escaped(step) not in below, step
    pilot = html.split('data-section="pilot"', 1)[1].split("</section>", 1)[0]
    assert escaped(text_of("p3.pilot.title")) in pilot
    assert "<ol" not in pilot and "<li" not in pilot
    assert pilot.count("<a ") == 1 and 'href="/' + lang + "/" in pilot


@pytest.mark.parametrize("state", ["closed", "open"])
def test_the_chapters_carry_one_section_device_and_no_running_head(request, page, seeded, state):
    """
    Every chapter under the hero opens the same way: the mark (the sprite's `ile-steps`, decorative), its title, its
    lead. No folio, no ordinal and no eyebrow: five of the seven running heads repeated the title under them or the
    link at the chapter's foot. Numerals are kept for the one real sequence (the neutral steps of the orientation
    while the gate is closed).
    """
    if state == "open":
        request.getfixturevalue("phase3_open")
    _response, html = page("/fr/")
    below = _under_the_hero(html)
    for gone in ('class="folio', "folio__ordinal", 'class="eyebrow"', "entry__ordinal", "section--process"):
        assert gone not in below, gone
    titled = re.findall(r'<h2 class="section__title" id="home-([a-z]+)-title"', below)
    assert titled, "the chapters have their titles"
    # the mark is the sprite's identity glyph, through the registry's tag: decorative, never mirrored
    marks = re.findall(
        r'<svg class="icon chapter__mark" aria-hidden="true" focusable="false"><use href="[^"]+#icon-([a-z-]+)">', below
    )
    assert marks == ["ile-steps"] * len(titled), "one mark per titled chapter, never two"
    assert below.count("chapter__mark") == len(titled) and "<path" not in below, "no drawing outside the sprite"
    # every chapter's forward link carries one arrow, mirrored on the Arabic page by its class
    for link in re.findall(r'<a class="link-arrow"[^>]*>.*?</a>', below, flags=re.S):
        assert link.count("#icon-arrow") == 1 and "icon--flip-rtl" in link, link


def test_a_sentence_the_hero_shows_is_given_back_when_the_hero_says_something_else(page, seeded):
    """The other half of «one thing once»: the trust chapter drops a fragment only while the hero prints it."""
    from cms.models import HeroVariant, HomeHero

    rows = HomeHero.objects.filter(variant=HeroVariant.INTERIM)
    updated = rows.update(body_fr="Une description écrite par la rédaction.")
    assert updated == 1, "the seeded interim hero is the row under test"
    _response, html = page("/fr/")
    block = html.split('data-section="trust"', 1)[1].split("</section>", 1)[0]
    assert escaped(text_of("p1.persons.replacement_1")) in block
    assert escaped(text_of("p1.persons.replacement_2")) in block


@pytest.mark.parametrize("state", ["closed", "open"])
def test_black_and_white_rests_only_in_the_hero(request, page, seeded, state):
    """
    DL54-12: the four audience photographs rest in black and white in the hero, and nowhere else. The chapters
    under the hero ship no photograph today (a partner's authorised logo apart), and their sheet sets no filter.
    """
    from pathlib import Path

    if state == "open":
        request.getfixturevalue("phase3_open")
    _response, html = page("/fr/")
    below = _under_the_hero(html)
    assert "<img" not in below and "<picture" not in below
    root = Path(__file__).resolve().parents[3]
    sheet = (root / "apps" / "pages" / "static" / "pages" / "css" / "pages.css").read_text(encoding="utf-8")
    assert "filter" not in re.sub(r"/\*.*?\*/", "", sheet, flags=re.S)
    hero_sheet = (root / "apps" / "pages" / "static" / "pages" / "css" / "hero.css").read_text(encoding="utf-8")
    assert ".he-plate__bw .he-photo { filter: grayscale(1)" in hero_sheet, "the black-and-white rest is the hero's"


# ---------------------------------------------------------------------------------------------
# Back-office composition: order, activation, publication, headings, translations
# ---------------------------------------------------------------------------------------------
def test_reordering_sections_changes_the_page(before_the_forum, page, seeded):
    HomeSection.objects.filter(key=SectionKey.TRUST).update(order=25)
    _response, html = page("/fr/")
    assert section_order(html) == ["hero", "banner", "trust", "entrances", "orientation", "pathways", "ecosystem"]


def test_disabling_a_section_removes_it(page, seeded):
    HomeSection.objects.filter(key=SectionKey.ORIENTATION).update(is_enabled=False)
    _response, html = page("/fr/")
    assert "orientation" not in section_order(html)
    assert 'id="home-orientation-title"' not in html


def test_unpublished_section_is_not_rendered(page, seeded):
    HomeSection.objects.filter(key=SectionKey.ECOSYSTEM).update(status=PublicationStatus.DRAFT)
    _response, html = page("/fr/")
    assert "ecosystem" not in section_order(html)


def test_editor_heading_is_rendered_and_tagged_french_elsewhere(page, seeded):
    HomeSection.objects.filter(key=SectionKey.TRUST).update(heading_fr="Notre engagement de transparence")
    _response, fr = page("/fr/")
    assert '<h2 class="section__title" id="home-trust-title">Notre engagement de transparence</h2>' in fr
    _response, it = page("/it/")
    assert '<h2 class="section__title" id="home-trust-title" lang="fr">Notre engagement de transparence</h2>' in it


def test_only_published_section_translations_are_rendered(page, seeded):
    from cms.models import TranslationStatus

    section = HomeSection.objects.get(key=SectionKey.TRUST)
    row = HomeSectionTranslation.objects.create(
        master=section, language="it", heading="Trasparenza (bozza)", status=TranslationStatus.DRAFT
    )
    _response, html = page("/it/")
    assert "Trasparenza (bozza)" not in html
    row.heading, row.status = "Cosa fa la piattaforma", TranslationStatus.PUBLISHED
    row.save()
    _response, html = page("/it/")
    assert '<h2 class="section__title" id="home-trust-title">Cosa fa la piattaforma</h2>' in html


def test_blank_heading_keeps_an_accessible_section_title(page, seeded):
    HomeSection.objects.filter(key=SectionKey.ENTRANCES).update(heading_fr="")
    _response, html = page("/fr/")
    assert '<h2 class="visually-hidden" id="home-entrances-title">' in html


def test_forbidden_formulation_typed_by_an_editor_is_never_rendered(page, seeded):
    HomeSection.objects.filter(key=SectionKey.TRUST).update(intro_fr="Un service de matching pour les entreprises")
    _response, html = page("/fr/")
    assert "matching" not in html.lower()


def test_homepage_works_before_the_sections_are_seeded(page, db):
    """A fresh install (no HomeSection row yet) still gets the prescribed composition."""
    assert not HomeSection.objects.exists()
    response, html = page("/fr/")
    assert response.status_code == 200
    assert html.count("<h1") == 1
    assert section_order(html)[0] == "hero"
    block = html.split('<ol class="register register--entrances', 1)[1].split("</ol>", 1)[0]
    assert block.count('<li class="register__item"') == 4


def test_homepage_query_budget(client, seeded, django_assert_max_num_queries):
    client.get("/fr/")  # warm the flag / settings caches
    with django_assert_max_num_queries(30):
        client.get("/fr/")
