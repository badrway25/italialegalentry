"""Homepage: composition, gates, prescribed texts, accessibility outline — in both gate states."""

from __future__ import annotations

import datetime as dt
import re

import pytest
from freezegun import freeze_time

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
    "news",
    "ecosystem",
    "reserved",
]


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
    # Prescribed texts have no official Arabic version: French, explicitly tagged.
    assert re.search(r'<h1 class="hero__title" id="hero-title"[^>]* lang="fr"', html)
    assert 'class="antifraud-panel__body" lang="fr"' in html


def test_french_home_has_no_fallback_lang_attributes_on_locked_texts(page, seeded, phase3_open):
    _response, html = page("/fr/")
    assert re.search(r'<h1 class="hero__title" id="hero-title"[^>]* translate="no"', html)
    assert not re.search(r'<h1 class="hero__title"[^>]* lang="', html)
    assert 'class="antifraud-panel__body">' in html


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
    assert '<script type="module" src="/static/pages/js/home.js"></script>' in html


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
    assert h1_text(hero) == text_of("p3.hero.title")
    assert escaped(text_of("p3.hero.subtitle")) in hero
    assert escaped(text_of("p3.hero.body")) in hero
    assert "Un écosystème pour les parcours réguliers" not in hero


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
    assert 'class="doorway__img"' in hero and 'class="doorway__key"' in hero and 'class="doorway__steps"' in hero
    assert "<figure" not in hero
    assert hero.count("<image ") == 2, "the photograph and the key, nothing else"


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

    for step in locked_content.get("p3.pilot.sequence", "fr")[0]:
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
    # site. What replaces them is an ordinal — a position in a register, which is information.
    assert not any("entrance-" in item and ".svg" in item for item in items)
    assert all('class="entry__ordinal"' in item for item in items)


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
    assert block.count('class="sequence__step') == 4
    assert "aria-current" not in block  # an explanation, not a progress state
    assert "pré-évaluation à caractère informatif" in block
    assert "autorités compétentes" in block
    assert 'href="/fr/orientation/"' in block


def test_orientation_phase3_uses_the_prescribed_sentence(page, seeded, phase3_open):
    _response, html = page("/fr/")
    block = html.split('data-section="orientation"', 1)[1].split("</section>", 1)[0]
    assert escaped(text_of("p3.persons.how_it_works")) in block
    assert 'class="sequence' not in block


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
    assert escaped(text_of("p1.persons.replacement_1")) in block
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
    assert "antifraud-panel" not in main
    assert "fraude" not in main.lower()  # no substitute text is invented


def test_antifraud_callout_links_the_page_when_open(page, seeded, phase3_open):
    _response, html = page("/fr/")
    block = html.split('data-section="antifraud"', 1)[1].split("</section>", 1)[0]
    assert escaped(text_of("p3.antifraud.title")) in block
    assert escaped(text_of("p3.antifraud.body")) in block
    assert 'href="/fr/attention-aux-fraudes/"' in block
    assert "#icon-shield" in block


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


def test_news_empty_state_when_open_without_articles(page, seeded, phase3_open):
    _response, html = page("/fr/")
    block = html.split('data-section="news"', 1)[1].split("</section>", 1)[0]
    assert 'class="empty-state"' in block
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
