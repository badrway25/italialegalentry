"""Homepage: composition, gates, prescribed texts, accessibility outline — in both gate states."""

from __future__ import annotations

import datetime as dt
import re

import pytest
from django.conf import settings
from freezegun import freeze_time

from cms import locked_content
from cms.forbidden import scan
from cms.models import PublicationStatus
from core import flags, icons
from pages.models import HomeSection, HomeSectionTranslation, SectionKey
from pages.tests.conftest import LANGS, PHASE3_HOME_KEYS, escaped, section_order, text_of
from tests.conftest import whatsapp_link_set_aside


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
    "ecosystem",
    "faq",
    "antifraud",
]  # no news chapter while no article is live (the review fix, m4): the tests that need it publish one
# RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (points 1 and 2): the home's
# narrative — the ecosystem and its promoter after «does / does not», the FAQ preview a section of its own, the warning
# against frauds the page's LAST section before the footer; the reserved closing row is no longer drawn (its access
# stays in the header: test_reserved_panel_* below). Stronger: the order is asserted whole, in the four languages.


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
    # Prescribed texts have no official Arabic version: French, explicitly tagged — in the V5 hero the h1 is the name,
    # visible (V5.12, the owner's Q1 answer), and the promise is the line under it, each a locked text. The promise
    # carries the fallback marker; the name is an English name on every page and says so, as the header's lock-up does
    # (a11y F10).
    assert re.search(r'<span class="he__name" id="hero-name" translate="no" dir="ltr" lang="en">', html)
    # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): the promise is compositional
    # (C-UI) — its provisional Arabic rendering, in the page's language; the anti-fraud body is substantive
    # (C-SUBST-FR) and the home is not its page — «la protezione» carries the Arabic pointer line, no French run
    from cms import locked_renderings

    promise = locked_renderings.rendering("p3.hero.subtitle")
    assert f'<p class="he__promise">{escaped(promise)}</p>' in html
    from django.utils import translation

    assert locked_renderings.treatment("p3.antifraud.body") == "C-SUBST-FR"
    with translation.override("ar"):
        pointer = str(locked_renderings.pointer_line("p3.antifraud.body"))
    assert pointer != text_of("p3.antifraud.body")
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B, «l'allerta»): the home draws its own warning band; the same body — the Arabic pointer line, no French
    # run — in its one <p data-locked>
    assert f'<p class="allerta__testo" data-locked="p3.antifraud.body">{escaped(pointer)}</p>' in html


def test_french_home_has_no_fallback_lang_attributes_on_locked_texts(page, seeded, phase3_open):
    _response, html = page("/fr/")
    # the name's own language is not a fallback marker: «Italy Legal Entry» is English on the French page too
    assert re.search(r'<span class="he__name" id="hero-name" translate="no" dir="ltr" lang="en">', html)
    assert not re.search(r'<h1 class="he__title[^"]*"[^>]* lang="', html)
    assert '<p class="he__promise">' in html
    # V5.22 (§0.1, «la protezione»; V5.20 strict rule): the same marker-free body, on the one anti-fraud plate
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B): the warning band's own body, with no fallback lang on the French page
    assert '<p class="allerta__testo" data-locked="p3.antifraud.body">' in html


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
    checked = whatsapp_link_set_aside(html)  # V5.19 §7: the owner's WhatsApp link only, as a link
    urls = re.findall(r'(?:src|href|srcset|content|action)="(https?://[^"]+)"', checked)
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
    # The V5 hero's one h1 is the locked name, VISIBLE (V5.12, the owner's Q1 answer: «Keep the visible H1 ITALY LEGAL
    # ENTRY™ … do not solve this by hiding the main title from sighted users»); the locked promise is the line under it
    # — each whole, character for character (HERO_FINAL.md §2.1; plan §1.17 «one brand expression»).
    name = re.search(r'<span class="he__name"[^>]*>(.*?)</span>', hero, flags=re.S).group(1)
    promise = re.search(r'<p class="he__promise"[^>]*>(.*?)</p>', hero, flags=re.S).group(1)
    assert name.strip() == escaped(text_of("p3.hero.title"))
    assert promise.strip() == escaped(text_of("p3.hero.subtitle"))
    assert h1_text(hero) == text_of("p3.hero.title")
    assert "visually-hidden he__name" not in hero
    # FINAL MICRO-PASS §5 A1 (V5.20 strict rule: the unbroken string gave way to the description's two voices): ONE
    # <p data-locked>, its statement and its supporting clause each a span, holds the locked text character for
    # character — its textContent is the text, cut once, nothing retyped
    assert _text_content(hero, '[data-locked="p3.hero.body"]') == [text_of("p3.hero.body")]
    assert len(re.findall(r'<span class="he__(?:enunciato|seguito)">', hero)) == 2
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


def test_a_plate_is_captioned_and_a_stock_frame_is_not(page, seeded):
    """
    Art direction A §6.2: a <figure> without a <figcaption> is a defect, and the caption must carry
    place, date, one factual sentence and a credit.

    V5.24 §2 (FINAL_DELIVERY_V2.md §3.2 D6; strict rule V5.20): the stock frames of the slot registry render no
    caption any more (the Pexels License requires no attribution; the author stays in PROVENANCE.json), so the
    count becomes two invariants — a curated plate (`figure.figura`) is captioned, a stock frame
    (`figure[data-slot]`) is not — the first as it was, the second new. v524-px-improve (the reviewer's m1; V5.20,
    stronger): the first is held on every figure that is NOT a stock frame, the exact complement of the second.

    This is the rule that makes anonymous stock photography structurally impossible rather than
    merely discouraged. The library inherited from the previous build does not pass it — six
    interchangeable frames served fifty-two pages, none captioned, none credited — so the home plate
    carries the page on type alone until a curated image exists. That is not a fallback: the
    direction requires the site to be recognisable with no photographs at all.
    """
    _response, html = page("/fr/")
    for attrs, body in re.findall(r"<figure\b([^>]*)>(.*?)</figure>", html, flags=re.S):
        if "data-slot=" not in attrs:
            assert "<figcaption" in body, "a curated plate ships with its caption"
        if "data-slot=" in attrs:
            assert "<figcaption" not in body and "Pexels" not in body, "a stock frame carries no credit"


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
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE PRECISION PASS of 11 Nov 2026 (§1–§3: the accesses'
    # descriptions come on intent, and on a phone by a real control): the NICHE still holds exactly one control, the
    # replay; the hero's only other buttons are the four accesses' disclosures — each a real button outside every
    # aria-hidden subtree, hidden until the script runs, closed, controlling the very sentence its link is described by
    niche = hero.split('<div class="he-niche" data-niche>', 1)[1]
    assert niche.count("<button") == 1
    more = re.findall(
        r'<button type="button" class="he-origin__more" data-origin-more aria-expanded="false" '
        r'aria-controls="(he-gloss-[a-z]+)" aria-label="[^"]+" hidden>',
        hero,
    )
    assert len(more) == 4 and len(set(more)) == 4 and hero.count("<button") == 5, more
    for gloss in more:
        assert hero.count(f'id="{gloss}"') == 1, "the sentence is in the document"
        assert re.search(rf'aria-describedby="{gloss} he-call-[a-z]+"', hero), "and it is the link's description"
        assert _aria_hidden_ancestors_of(hero, f'aria-controls="{gloss}"') == []
        assert _aria_hidden_ancestors_of(hero, f'id="{gloss}"') == []
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


#: the locked texts the V2 home re-composes at render (V5.22, SECTION_SYSTEM_V2 §1 rule 6): set in typographic levels by
#: spans cut on their own separators — the anti-fraud body on its full stops («la protezione»), each trust answer's
#: «Non.» as the large keyword, the promoter's answer with two ink keywords — so the text runs in the page as the
#: element's textContent, character for character (cms.locked_split), not as one unbroken string of the source.
#: V5.22 round 1 (QA_ROUND1 m5; §1 rule 6, an approved decision: a locked text is re-composed at render by spans; V5.20
#: strict rule): the pilot's title keeps «VÉNÉTIE–MAROC» on one line by a render-time span (cms.locked_split.emphasize)
#: — held to its heading's textContent, exactly the locked title: the same text, now checked as the whole element
RECOMPOSED = {"p3.antifraud.body", "p3.pilot.title", "p3.hero.body"}  # FINAL MICRO-PASS §5 A1: the hero's two voices


def _text_content(html: str, selector: str) -> list[str]:
    from bs4 import BeautifulSoup

    return [node.get_text() for node in BeautifulSoup(html, "html.parser").select(selector)]


def test_phase3_prescribed_texts_present_when_open(page, seeded, phase3_open):
    """Every Phase 3 text of the home is on the page, verbatim. V5.22 (V5.20 strict rule): a text the V2 home sets in
    typographic levels is held to its element's textContent — exactly the locked text, each split checked whole —, the
    others to the unbroken string as before."""
    _response, html = page("/fr/")
    for key in PHASE3_HOME_KEYS:
        if key in RECOMPOSED:
            continue
        if key.startswith("p3.reserved."):
            # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 2): the reserved row's
            # prescribed texts leave the home with the row — asserted ABSENT from the page's body, so the row cannot
            # silently return; every other Phase 3 text of the home is still held verbatim
            assert escaped(text_of(key)) not in html.split('<main id="main-content"', 1)[1], key
            continue
        assert escaped(text_of(key)) in html, key
    assert _text_content(html, '[data-locked="p3.antifraud.body"]') == [text_of("p3.antifraud.body")]
    assert _text_content(html, "#home-pilot-title") == [text_of("p3.pilot.title")]
    assert _text_content(html, '[data-locked="p3.hero.body"]') == [text_of("p3.hero.body")]
    from cms import locked_content

    # The pilot sequence is on the page where the hero's path carries it (its second to sixth steps, after the
    # origin's shore): the chapters under the hero do not print it a second time (below: the model is said once).
    for step in locked_content.get("p3.pilot.sequence", "fr")[0][1:6]:
        assert escaped(step) in html
    for pathway in locked_content.get("p3.persons.pathways", "fr")[0]:
        assert escaped(pathway["title"]) in html
        assert escaped(pathway["description"]) in html
    faq = {item["key"]: item for item in locked_content.get("p3.faq.items", "fr")[0]}
    for key in ("faq_visas", "faq_recruitment_agency", "faq_preassessment_guarantee", "faq_diplomas"):
        # the plate's answer: «Non.» the keyword, the rest after it — one <p>, its text the answer itself
        assert _text_content(html, f'[data-faq="{key}"] .integrita__risposta') == [faq[key]["answer"]], key
        assert _text_content(html, f'[data-faq="{key}"] .ls-1') == ["Non. "], key
    assert _text_content(html, '[data-faq="faq_who"]') == [faq["faq_who"]["answer"]]


def test_the_arabic_pilot_title_keeps_its_bytes_and_isolates_its_french_name(page, seeded, phase3_open):
    """The owner's FINAL CLOSURE PASS of 12 Nov 2026: the prescribed Arabic rendering «المشروع التجريبي
    Vénétie–Maroc» is never reworded — the heading's textContent is the locked text byte for byte — and its French
    proper name is ONE left-to-right unit (<bdi dir="ltr">, no lang: a Latin lang on the heading's only element child
    would turn the whole heading left to right), so the dash is never reordered and the Arabic phrase reads right to
    left; French keeps its one-line span."""
    from cms import locked_content

    _response, html = page("/ar/")
    text, lang = locked_content.get("p3.pilot.title", "ar")
    assert lang == "ar"
    assert _text_content(html, "#home-pilot-title") == [text]
    title = html.split('id="home-pilot-title"', 1)[1].split("</h2>", 1)[0]
    assert '<bdi class="em-keyword" dir="ltr">Vénétie–Maroc</bdi>' in title, title
    _response, html = page("/fr/")
    title = html.split('id="home-pilot-title"', 1)[1].split("</h2>", 1)[0]
    assert '<span class="em-keyword">VÉNÉTIE–MAROC</span>' in title, title


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
    # V5.22 (SECTION_SYSTEM_V2 §3.1 S1, §2 J «il passaggio»; V5.20 strict rule): the four doors are the plates of a
    # phone's rail — an <ol class="passaggio">, each <li> its route and its audience
    block = html.split('<ol class="passaggio', 1)[1].split("</ol>", 1)[0]
    return block.split('<li class="passaggio__lastra"')[1:]


def test_exactly_four_entrances_gate_closed(page, seeded):
    _response, html = page("/fr/")
    assert html.count('<ol class="passaggio') == 1
    items = _entrances(html)
    assert len(items) == 4
    titles = [re.search(r'class="passaggio__titolo"[^>]*>([^<]+)<', item).group(1) for item in items]
    assert titles == ["Personnes", "Entreprises", "Institutions", "Universités et organismes de formation"]
    targets = [re.search(r'class="passaggio__porta" href="([^"]+)"', item).group(1) for item in items]
    assert targets == [
        "/fr/parcours/",
        "/fr/entreprises/recueil-des-besoins/",
        "/fr/collaboration/institutions/",
        "/fr/collaboration/universites-formation/",
    ]
    # The four line drawings are retired with the cards that carried them, and the four are never ranked: no ordinal
    # 01–04, no landform glyph nobody could decode, one arrow beside the call's words. V5.22 (SECTION_SYSTEM_V2 §3.1 S1,
    # §4.2 T2a — an approved decision; V5.20 strict rule): each door's arched seat holds its AUDIENCE's disc — the
    # registry's glyph of that actor and no other, decorative —, so a plate names its door twice over, never a rank.
    # RESTATED under V5.20 for the FINAL MICRO-PASS's review (10 Nov 2026, defect 1: on a phone the four arched seats
    # and their discs were the page's arches after the hero's door): no seat, no arch, no disc, no glyph but the call's
    # arrow — and every plate still says its prescribed question, its sentence and its call.
    assert not any("entrance-" in item and ".svg" in item for item in items)
    assert not any("entry__ordinal" in item or "route__glyph" in item or "linea__num" in item for item in items)
    assert all(item.count("#icon-arrow") == 1 and 'class="passaggio__cta"' in item for item in items)
    for item, actor in zip(items, ("person", "company", "institution", "university")):
        glyphs = re.findall(r'#icon-([a-z0-9-]+)"', item)
        assert glyphs == ["arrow"], (actor, glyphs)
        assert not re.search(r"passaggio__seggio|passaggio__arco|sez-disc|<mask", item), actor
        assert 'class="passaggio__titolo"' in item and 'class="passaggio__testo"' in item, actor


def test_exactly_four_entrances_phase3_open_with_prescribed_texts(page, seeded, phase3_open):
    _response, html = page("/fr/")
    items = _entrances(html)
    assert len(items) == 4
    for item, actor in zip(items, ("person", "company", "institution", "university")):
        assert escaped(text_of(f"p3.entrances.{actor}.title")) in item
        assert escaped(text_of(f"p3.entrances.{actor}.text")) in item
        assert escaped(text_of(f"p3.entrances.{actor}.button")) in item
        assert 'class="passaggio__porta" href="/fr/' in item  # every entrance resolves to a page
    assert "/fr/parcours/" in items[0]


def test_entrances_are_h3_under_the_section_h2(page, seeded):
    _response, html = page("/fr/")
    # V5.22 (V5.20 strict rule): the V2 head (components/sezioni/_testa.html) and the doors' titles — the same outline
    assert '<h2 class="testa__title" id="home-entrances-title">' in html
    assert html.count('<h3 class="passaggio__titolo"') == 4


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
    # the four neutral steps on the public passage (W3-D: components/stepper.html), across from 48rem — V5.22
    # (SECTION_SYSTEM_V2 §3.1 S2 «gate closed: the neutral four steps on the same route», §1 rule 8; V5.20 strict rule):
    # the passage evolved, «la linea V2» (size="large"), the same pattern in both gate states, the editorial note as
    # the route's terminal line. FINAL MICRO-PASS §5 A1/A2 (V5.20 strict rule: the seal at station 1 and the tiles of
    # stations 2 to 4 left): each station is its quiet sequence marker and its words — no seal, no tile, no glyph —,
    # the four words still there
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§10–§11, lane B «il viaggio»): the four steps are four moments — real tabs, each its keyword and its semantic
    # glyph — beside the stage; no numeral, no seal; the four neutral words still there, in order
    assert block.count('class="viaggio__voce"') == 4 and block.count('class="viaggio__scena"') == 4
    assert "linea__num" not in block and "sigillo" not in block and "sez-tile" not in block
    glyphs = re.findall(
        r'<span class="viaggio__glifo" aria-hidden="true"><svg [^>]*><use href="[^"#]*#icon-([a-z-]+)"', block
    )
    assert glyphs == ["compass", "list-checks", "book-open", "scroll-text"], glyphs
    labels = re.findall(r'<span class="viaggio__parole">([^<]+)</span>', block)
    assert len(labels) == 4 and all(label.strip() for label in labels)
    assert "aria-current" not in block and "linea__rank" not in block  # an explanation, not a progress state
    assert "pré-évaluation à caractère informatif" in block
    assert "autorités compétentes" in block
    assert 'href="/fr/orientation/"' in block


def test_orientation_phase3_uses_the_prescribed_sentence(page, seeded, phase3_open):
    """V5.22 (SECTION_SYSTEM_V2 §3.1 S2, §2 F; V5.20 strict rule — the old expectation, the sentence set whole and no
    passage, conflicts with the approved decision to draw it as «la linea V2»): the locked sentence is cut on its own
    separators by the owner-approved cut (D-U4, pathways.services.how_it_works, which returns None unless the parts
    rebuild it character for character) — its lead the caption, its four steps the stations, its caveat the terminal
    line — and it is said ONCE, whole, for a screen reader, the drawn parts hidden from it. Stronger than before: the
    whole sentence is present once, and every drawn part is exactly a part of it."""
    from pathways.services import how_it_works

    _response, html = page("/fr/")
    block = html.split('data-section="orientation"', 1)[1].split("</section>", 1)[0]
    sentence = text_of("p3.persons.how_it_works")
    assert block.count(escaped(sentence)) == 1
    assert f'<p class="visually-hidden">{escaped(sentence)}</p>' in block
    cut = how_it_works("fr")
    assert cut is not None and cut.text == sentence
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B «il viaggio»): the stations are drawn in the four moments' tabs and on their stage, each exactly a part
    # of the sentence, hidden from a screen reader that has heard it whole
    labels = re.findall(r'<span class="viaggio__parole" aria-hidden="true">([^<]+)</span>', block)
    assert labels == [escaped(step) for step in cut.steps]
    staged = re.findall(r'<span class="viaggio__frase">([^<]+)</span>', block)
    assert staged == labels and block.count('<div class="viaggio__didascalia" aria-hidden="true">') == 4
    # FINAL MICRO-PASS §5 A1 (V5.20 strict rule: the caption drawn for the eye left — the section's head says what the
    # route is): the lead is no longer drawn apart, and it is still said, inside the whole sentence, once
    assert "orienta__didascalia" not in block and "orienta__portico" not in block
    assert escaped(cut.lead) in escaped(sentence) and block.count(escaped(sentence)) == 1
    assert f'<p class="orienta__avvertenza" aria-hidden="true">{escaped(cut.caveat)}</p>' in block
    assert "aria-current" not in block and 'class="sequence' not in block


def test_pathways_gate_closed_shows_neutral_families_only(page, seeded):
    _response, html = page("/fr/")
    block = html.split('data-section="pathways"', 1)[1].split("</section>", 1)[0]
    # V5.22 (SECTION_SYSTEM_V2 §3.1 S3 «gate closed: the neutral families as a static index (no stage, no
    # destination)»; V5.20 strict rule): the five families as still rows of the index — no stage, no tab, no link
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (lane B): the five families as still chips — no stage, no tab, no link to a sheet
    assert block.count('class="home-families__voce"') == 5
    assert 'class="esplora__palco' not in block and "data-tabs" not in block and 'data-sec-js="indice"' not in block
    assert 'class="pathway-list"' not in block
    assert 'href="/fr/parcours/"' in block
    from cms import locked_content

    for pathway in locked_content.get("p3.persons.pathways", "fr")[0]:
        assert escaped(pathway["description"]) not in html


def test_pathways_phase3_lists_the_eight_prescribed_pathways(page, seeded, phase3_open):
    _response, html = page("/fr/")
    # the stage's panels are <section>s of their own: the block runs to the next section of the page
    block = html.split('data-section="pathways"', 1)[1].split("data-section=", 1)[0]
    assert 'data-pathways="8"' in block
    # V5.22 (SECTION_SYSTEM_V2 §3.1 S3, §2 L «l'indice»; V5.20 strict rule): eight rows of the index, each the
    # registry's PATHWAY glyph and the prescribed title, and eight panels on the stage, in the locked order (never a
    # ranking) — every description in the page
    entries = locked_content.get("p3.persons.pathways", "fr")[0]
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§14, lane B «l'esploratore»): the explorer's index rail, each row its toned glyph tile and its prescribed
    # title, and eight stage panels, in the locked order
    rows = re.findall(r'<a class="esplora__voce" id="parcours-([a-z-]+)-tab" href="#parcours-\1"', block)
    assert len(rows) == 8 and [row.replace("-", "_") for row in rows] == [entry["key"] for entry in entries]
    assert block.count('<section class="esplora__pannello"') == 8
    glyphs = re.findall(
        r'<span class="esplora__tessera" aria-hidden="true"><svg class="icon"[^>]*><use href="[^"#]*#icon-([a-z-]+)"',
        block,
    )
    assert glyphs == [icons.PATHWAY[entry["key"]] for entry in entries]
    for entry in entries:
        assert escaped(entry["description"]) in block


def test_trust_gate_closed_uses_phase1_fragments_and_neutral_statements(page, seeded):
    _response, html = page("/fr/")
    block = html.split('data-section="trust"', 1)[1].split("</section>", 1)[0]
    assert 'data-trust="interim"' in block
    # One thing once (pages.services._say_once): the hero's description IS the first of the two Phase 1 fragments,
    # so the chapter lists the other one and does not print the hero's sentence a second time.
    assert escaped(text_of("p1.persons.replacement_1")) not in block
    assert html.count(escaped(text_of("p1.persons.replacement_1"))) == 1
    assert escaped(text_of("p1.persons.replacement_2")) in block
    # V5.22 (SECTION_SYSTEM_V2 §3.1 S5 «gate closed: the interim two lists become two plates»; V5.20 strict rule)
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§19, lane B «la chiarezza»): the two lists are the two material surfaces, does / does not
    assert len(re.findall(r'<article class="[^"]*\bchiaro__faccia\b', block)) == 2
    # V5.14 C/D (lane C's M-2; the steward, the v515-c merge): the unpublished disclaimer answers 404, so no link to it
    assert 'href="/fr/avvertenze/"' not in block


def test_trust_phase3_quotes_four_prescribed_faq_entries(page, seeded, phase3_open):
    _response, html = page("/fr/")
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§20, lane B «le domande»): the four entries are the FAQ preview's band.
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 1): the preview is a section
    # of its own (data-section="faq"), after the ecosystem — the same four entries, in the same order, in its block,
    # which runs to the warning that closes the page
    block = html.split('data-section="faq"', 1)[1].split('data-section="antifraud"', 1)[0]
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
    # V5.22 (§1 rule 6, «la protezione»; V5.20 strict rule): the body in three levels — its element's text is the
    # locked body itself, character for character
    assert _text_content(block, '[data-locked="p3.antifraud.body"]') == [text_of("p3.antifraud.body")]
    assert 'href="/fr/attention-aux-fraudes/"' in block
    # one sign for one warning — V5.22 (SECTION_SYSTEM_V2 §0.1 «one locked text gets one rendering», §4.9 n.9; V5.20
    # strict rule): «la protezione», the same plate on every page, signs the warning with the ILE shield `ile-scudo`,
    # once; never the account-security shield. FINAL MICRO-PASS §5 A3: the shield is drawn bare — no arch seat
    assert 'class="sigillo' not in block and "data-sigillo-scope" not in block and "data-mark=" not in block
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§11 «Fraud → shield/warning», §22, lane B «l'allerta»): the band's one large sign is the semantic shield-alert,
    # once, beside the locked title; never the account-security shield; the red flags are UI chips, never numbered
    assert block.count('<span class="allerta__scudo" aria-hidden="true">') == 1
    assert block.count("#icon-shield-alert") == 1 and '#icon-shield"' not in block
    assert block.count("<li>") == 5 and "<ol" not in block


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
    is empty (DL54-33: the news' glyph, never the documents'). V5.12 §8: the news' own page no longer keeps an empty
    state — it answers 404 until an article is live, and nothing links to it."""
    _response, html = page("/fr/")
    assert 'data-section="news"' not in html
    assert "Aucune actualité publiée" not in html
    assert 'href="/fr/actualites/"' not in html


def test_news_section_appears_in_phase3_once_an_article_is_published(page, seeded, phase3_open, article_factory):
    article_factory("Programme du Forum publié")
    _response, html = page("/fr/")
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 1): the news stands between
    # the FAQ preview and the warning, which stays the last section
    assert section_order(html) == [*OPEN_ORDER[:8], "news", *OPEN_ORDER[8:]]
    assert section_order(html)[-1] == "antifraud"
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
def test_ecosystem_shows_the_promoter_alone_without_an_authorised_partner(page, seeded):
    """V5.12 §8: no «partners presented as they authorise» sentence and no link to an empty partners' page — the
    promoter's bay stands alone, at the full width."""
    _response, html = page("/fr/")
    block = html.split('data-section="ecosystem"', 1)[1].split("</section>", 1)[0]
    assert "AGAMI — Dialogo Giuridico Interculturale APS" in block
    assert "home-ecosystem__grid--single" in block and "home-ecosystem__partners" not in block
    assert "au fur et à mesure" not in block
    assert 'href="/fr/agami/"' in block and 'href="/fr/partenaires/"' not in block
    # no logo, authorised or not, without a written authorisation: the bay's one photograph is the V5.12 working-table
    # (slot «home.ecosystem», DECISIONS §6), no credit (V5.24 §2). RESTATED under V5.20 for the owner's FINAL
    # HOMEPAGE REBUILD directive of 10 Nov 2026 (§25,
    # lane A): the promoter's band also draws the PROMOTER'S OWN two marks (pages.imagery.MARKS, PROVENANCE.json — the
    # /agami/ page's), and nothing else: still no partner's logo, and exactly three images, each accounted for
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 3: «the identity appears
    # twice»): ONE AGAMI mark — the official rectangular lockup; the round seal left the band. Stronger: exactly two
    # images, each accounted for, and the seal asserted absent
    assert block.count("<img") == 2 and block.count('data-slot="home.ecosystem"') == 1
    assert block.count('data-mark="agami.insegna"') == 1 and "agami.sigillo" not in block
    assert block.count("<picture") == 2
    assert "home-ecosystem__logo" not in block


def test_ecosystem_lists_only_authorized_partners(page, seeded, partner_factory):
    partner_factory("Université partenaire autorisée")
    partner_factory("Organisme non autorisé", authorized=False)
    partner_factory("Partenaire en brouillon", status=PublicationStatus.DRAFT)
    _response, html = page("/fr/")
    assert "Université partenaire autorisée" in html
    assert "Organisme non autorisé" not in html
    assert "Partenaire en brouillon" not in html


def test_reserved_panel_needs_phase3_and_flag(page, seeded, set_flag, phase3_open):
    """RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 2: the closing row
    repeated the header's «Espace réservé» and the pathways' Espace Personnes): with the gate open and the flag on, the
    home draws NO reserved row — no section, none of its prescribed sentence, no seal — and the access stays where it
    already was, in the header (the same login page). The builder still answers (the row is reversible:
    pages.services.HOME_OMITS), and it still needs Phase 3 and the flag."""
    from pages import services

    _response, html = page("/fr/")
    assert 'data-section="reserved"' not in html and "home-reserved" not in html
    assert escaped(text_of("p3.reserved.body")) not in html
    assert section_order(html)[-1] == "antifraud"  # the warning is the page's last word before the footer
    header = html.split('<main id="main-content"', 1)[0]
    assert re.search(r'<a class="targa[^"]*" href="/fr/compte/login/"', header), "the access stays in the header"
    assert SectionKey.RESERVED in services.HOME_OMITS and SectionKey.RESERVED in services.BUILDERS
    ctx = services.BuildContext(request=None, lang="fr", phase3=True)
    built = services.build_reserved(ctx)
    assert built["url"] == "/fr/compte/login/" and str(built["title"]) == text_of("p3.reserved.title")
    # the row's sign is the key of the mark, never a padlock — V5.22 (SECTION_SYSTEM_V2 §3.1 S8, §4.2 T5; V5.20 strict
    # rule): the T5 `ile-accesso`, the key standing in the doorway's opening, in its night arch seat, once. V5.30
    # stream A
    # (the owner's «geometry saturation»; V5.20 strict rule: the same seat, now named): the seat is a quiet tile unless
    # the caller asks for the arch, and this row, one of the brand's two bookends, asks for it
    assert 'data-mark="ile-accesso"' not in html.split('<main id="main-content"', 1)[1], "no seal on the home"
    assert "#icon-lock" not in html
    set_flag("reserved_area_public_link", False)
    assert services.build_reserved(ctx) is None, "the row's builder still needs the flag"
    _response, html = page("/fr/")
    assert 'data-section="reserved"' not in html
    assert escaped(text_of("p3.reserved.body")) not in html


def test_reserved_panel_links_dashboard_for_signed_in_visitor(client, seeded, phase3_open, person_user):
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 2): no reserved row on the
    # home for a signed-in visitor either; the way to the dashboard is the header's, as on every page
    client.force_login(person_user)
    html = client.get("/fr/").content.decode()
    assert 'data-section="reserved"' not in html
    assert 'href="/fr/espace-reserve/"' in html.split('<main id="main-content"', 1)[0]


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
    # V5.22 round 1 (QA_ROUND1 m5, §1 rule 6; V5.20 strict rule): the title is re-composed by a render-time span — held
    # to its heading's textContent, exactly the locked title
    # V5.27 (FINAL_DELIVERY_V2 R7′; V5.20, the steward's amendment at the v524-ar merge): the Arabic title is its
    # provisional rendering, held the same way
    expected = locked_content.get("p3.pilot.title", lang)[0] if lang == "ar" else text_of("p3.pilot.title")
    assert _text_content(pilot, "#home-pilot-title") == [expected]
    assert "<ol" not in pilot and "<li" not in pilot
    assert pilot.count("<a ") == 1 and 'href="/' + lang + "/" in pilot


#: the T1 seals the V2 home draws (V5.22, SECTION_SYSTEM_V2 §3.1, §4.2, §4.8): the orientation's at its route's origin
#: (gate G3 open or closed: the same route), «la protezione»'s on its rule, the reserved row's key — each once a page
#: FINAL MICRO-PASS §5 A1/A3 (V5.20 strict rule): the orientation's seal and «la protezione»'s arch seat left (the
#: route is its quiet markers, the shield is drawn bare); the reserved row's key stays — once
# RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 2): the reserved row's key was
# the home's last seal — under the hero the home draws no seal in either gate state (stronger)
HOME_SEALS = {"closed": [], "open": []}


@pytest.mark.parametrize("state", ["closed", "open"])
def test_the_sections_open_with_one_head_and_no_glyph_above_a_title(request, page, seeded, state):
    """
    V5.22 (SECTION_SYSTEM_V2 §0 item 3, §2.0 «Head roles», §4.1 rule 1 — the owner's V5.22 §6: «the current tiny
    icons placed above headings are not visually strong enough»; V5.20 strict rule: the old expectation, one concept
    mark above each chapter title, conflicts with that approved decision): under the hero no section draws a glyph
    above its title. Each opens with the V2 head (components/sezioni/_testa.html: its drawn rule, its title, its lead),
    and a section's theme, when it has one, is a T1 seal INSIDE its composition — the orientation's at its route's
    origin, «la protezione»'s on its rule, the key in the reserved row —, each once, never the journey's stair. What
    V5.12 and W2-D held stays held: no folio, ordinal or eyebrow, numerals for the one real sequence only, every
    forward link with its one arrow mirrored on the Arabic page, every drawing decorative.
    """
    if state == "open":
        request.getfixturevalue("phase3_open")
    _response, html = page("/fr/")
    below = _under_the_hero(html)
    for gone in ('class="folio', "folio__ordinal", 'class="eyebrow"', "entry__ordinal", "section--process"):
        assert gone not in below, gone
    for gone in ("chapter__mark", "chapter__head", 'class="section__title"', 'class="chapter '):
        assert gone not in below, (gone, "the chapter device leaves the home")
    titled = re.findall(r'<h2 class="testa__title" id="home-([a-z]+)-title"', below)
    assert titled, "the sections have their heads"
    for head in re.findall(r'<div class="testa testa--[a-z]+">(.*?)</h2>', below, flags=re.S):
        assert "<svg" not in head and "sigillo" not in head, "no glyph stacked above a title"
    seals = re.findall(r'<span class="sigillo [^"]*" data-mark="([a-z-]+)"', below)
    assert seals == HOME_SEALS[state], seals
    assert "ile-steps" not in below, "the stair is the journey's (V5.12 §7)"
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026
    # (§1, §10: «not 1 2 3 4»): no numeral marks anything under the hero — the orientation's moments are glyphs
    assert "linea__num" not in below and "linea__step" not in below, "no numeral marker under the hero"
    # every inline drawing under the hero is decorative — the seals' marks, the portico, the doors' arches, the threads
    for svg in re.findall(r"<svg\b[^>]*>", below):
        assert 'aria-hidden="true"' in svg, svg
    # every section's forward link carries one arrow, mirrored on the Arabic page by its class
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
    DL54-12: the four audience photographs rest in black and white in the hero, and nowhere else at rest. V5.12
    (DECISIONS §6) adds three V5 frames under the hero — the pilot's diptych and the ecosystem's table — drawn only
    through the slot registry ({% photo %}): the diptych alone «develops» from black and white to colour as it enters
    the view (v5/_photo.css, a scroll-driven animation: colour at rest once in view, and from the start under reduced
    motion); the home's own sheet still sets no filter.
    """
    from pathlib import Path

    if state == "open":
        request.getfixturevalue("phase3_open")
    _response, html = page("/fr/")
    below = _under_the_hero(html)
    pictures = re.findall(r'<figure class="foto[^"]*" data-slot="([^"]+)"([^>]*)>', below)
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§9, §25, §28; lanes A and
    # B merged): under the hero every picture is a registry's — the slot registry's frames, AGAMI's own two marks
    # (pages.imagery.MARKS: drawn whole, never graded, never masked: asserted here) in the promoter's band, and the
    # <picture>s the orientation's moments and the explorer's stage draw themselves (colour, lazy, never graded);
    # nothing else draws a picture under the hero
    marks = re.findall(r'<picture class="[^"]*" data-mark="([^"]+)"[^>]*>', below)
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 3): ONE AGAMI mark, the
    # official lockup — the round seal left the promoter's band
    assert sorted(marks) == ["agami.insegna"]
    own = re.findall(r'<picture class="(?:viaggio__foto|esplora__foto)"', below)
    assert below.count("<picture") == len(pictures) + len(marks) + len(own)
    for mark in re.findall(r'<picture class="[^"]*" data-mark="[^"]+".*?</picture>', below, flags=re.S):
        assert "data-grade" not in mark and "data-reveal" not in mark and "grayscale" not in mark
    assert not re.findall(r'<picture class="(?:viaggio__foto|esplora__foto)"[^>]*data-grade', below)
    slots = {slot for slot, _attrs in pictures}
    # V5.22 (SECTION_SYSTEM_V2 §8 «Treatments», §8.1; V5.20 strict rule, the set extended as the Director's §8 asks,
    # citing V5.22 §14): the integrity band's ground — dressed stone, desaturated IN THE FILE, decorative, never a CSS
    # grayscale — joins the three frames; the invariant stands: black and white rests only in the hero
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE REBUILD directive of 10 Nov 2026 (§8, lane A): the
    # ecosystem's introduction under the hero draws the
    # Réseau page's working table (network.table, its «intro» variant, a lazy body frame), in colour — never graded
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE PRECISION PASS of 11 Nov 2026 (§9–§10: «replace the intro
    # image»): the introduction draws its OWN frame (home.intro: two people over the same file), no longer the Réseau
    # page's table — same invariant, stronger: the home borrows no other page's head frame here, and the frame is in
    # colour, never graded
    allowed = {"home.pilot.cedar", "home.pilot.marble", "home.ecosystem", "home.integrity.stone", "home.intro"}
    assert slots <= allowed, slots
    assert "network.table" not in slots
    assert not [
        attrs for slot, attrs in pictures if slot in ("home.integrity.stone", "home.intro") and "data-grade" in attrs
    ]
    # the W2 review's M-3: the black-and-white rest is lane A's one mechanism (data-grade, v5/_reveal.css), on the
    # diptych only; every frame under the hero is masked as it enters (data-reveal="mask")
    assert {slot for slot, attrs in pictures if 'data-grade="bw-scroll"' in attrs} <= {
        "home.pilot.cedar",
        "home.pilot.marble",
    }
    assert all('data-reveal="mask"' in attrs for _slot, attrs in pictures)
    reveal_sheet = (Path(__file__).resolve().parents[3] / "static" / "css" / "v5" / "_reveal.css").read_text(
        encoding="utf-8"
    )
    assert "prefers-reduced-motion: no-preference" in reveal_sheet and 'html.rm [data-grade|="bw"] img' in reveal_sheet
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
    # V5.22 (V5.20 strict rule): the V2 head (components/sezioni/_testa.html) — the same title, tagged French elsewhere
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 5: the section's title and
    # its two surfaces' heads said the same thing twice): the editor's heading is still the section's ONE h2, named by
    # the section (aria-labelledby), tagged French elsewhere — in the outline only while the section opens on its lead
    assert '<h2 class="visually-hidden" id="home-trust-title">Notre engagement de transparence</h2>' in fr
    assert fr.count('id="home-trust-title"') == 1 and 'aria-labelledby="home-trust-title"' in fr
    _response, it = page("/it/")
    assert '<h2 class="visually-hidden" id="home-trust-title" lang="fr">Notre engagement de transparence</h2>' in it


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
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE VISUAL QA of 11 Nov 2026 (point 5): the published
    # translation is the section's ONE h2 (the V2 head, or the outline's title while the section opens on its lead)
    assert re.search(
        r'<h2 class="(?:testa__title|visually-hidden)" id="home-trust-title">Cosa fa la piattaforma</h2>', html
    )
    assert html.count('id="home-trust-title"') == 1


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
    # V5.22 (V5.20 strict rule): the four doors on their rail (S1 «il passaggio»)
    block = html.split('<ol class="passaggio', 1)[1].split("</ol>", 1)[0]
    assert block.count('<li class="passaggio__lastra"') == 4


def test_homepage_query_budget(client, seeded, django_assert_max_num_queries):
    client.get("/fr/")  # warm the flag / settings caches
    with django_assert_max_num_queries(30):
        client.get("/fr/")


def test_the_home_shows_the_name_once(page, seeded, phase3_open):
    """V5.12 Q1: one name on the screen, never the wordmark twice one under the other.

    RESTATED under V5.20 for the owner's FINAL HOMEPAGE PRECISION PASS of 11 Nov 2026 (§16–§21: the header's lock-up
    must READ «Italy Legal Entry» on the home too). Old invariant: the hero's sheet hid the header's words on the
    home, the H1 was the one visible name. New invariant, the same promise at every width: the name is read once —
    in the header wherever its lock-up draws the words (20.51–63.999 rem and from 76 rem), where the hero's H1 keeps
    its place in the outline with no box; in the hero's H1 where the header is the mark alone (64–75.999 rem and at
    most 20.5 rem). The two ranges are complementary, and the hero's sheet no longer hides the header's words."""
    _response, html = page("/fr/")
    assert (
        'class="brand brand--lockup"' in html and "aria-label=" in html.split('class="brand brand--lockup"', 1)[1][:200]
    )
    assert html.count("<h1") == 1 and 'class="he__title he__title--name" id="hero-title"' in html
    dist = settings.BASE_DIR / "static" / "css" / "dist"
    hero = (dist / "pages" / "css" / "hero.css").read_text(encoding="utf-8")
    assert ".site-header .lock__text{display:none}" not in hero
    main = (dist / "main.css").read_text(encoding="utf-8")
    # RESTATED under V5.20 for the owner's FINAL HOMEPAGE ART-DIRECTION + TYPOGRAPHY PASS of 11 Nov 2026 (A4: «the FULL
    # lockup … visible and readable … INCLUDING 1024–1215 px»): the 64–75.999 rem band no longer draws the mark alone,
    # so the header reads the name at EVERY width above 20.5 rem, and the hero's H1 keeps no box at all of them. Was:
    # two ranges (20.51–63.999 rem and from 76 rem) and the mark alone between. Now one range from 20.51 rem, the
    # complement (at most 20.5 rem: the mark alone, the H1 the one name) unchanged — still exactly one name on screen
    drawn = "(min-width:20.51rem)"
    assert f"@media{drawn}{{.he__title--name{{block-size:0;overflow:hidden}}" in main, "no box where the header reads"
    assert "@media(max-width:20.5rem){.lock__text{display:none}" in main
    assert main.count(".lock__text{display:none}") == 1, "the only band that hides the header's name is ≤ 20.5 rem"
    assert "brand--lockup .lock__text{display:none}" not in main
