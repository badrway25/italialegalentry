"""Unit tests of pages.services: editorial strings, locked references, photographs, link targets."""

from __future__ import annotations

import pytest
from django.utils import translation

from cms import locked_content
from cms.models import HeroVariant, HomeHero, MediaAsset, PublicationStatus
from pages import content, services
from pages.models import HomeSection, SectionKey

pytestmark = pytest.mark.django_db


# ---- editorial strings --------------------------------------------------------------------------
def test_editorial_in_french_has_no_lang_attribute():
    with translation.override("fr"):
        text = services.editorial("Un titre rédigé par l’équipe")
    assert (text.value, text.lang) == ("Un titre rédigé par l’équipe", "")


def test_editorial_untranslated_value_is_tagged_french_on_other_languages():
    with translation.override("en"):
        text = services.editorial("Un titre sans traduction connue 123")
    assert (text.value, text.lang) == ("Un titre sans traduction connue 123", "fr")


def test_editorial_empty_value_never_returns_the_po_header():
    with translation.override("it"):
        assert not services.editorial("")
        assert str(services.editorial("   ")) == ""


def test_editorial_drops_forbidden_formulations():
    with translation.override("fr"):
        assert not services.editorial("Le meilleur matching pour votre entreprise")
        assert not services.editorial("Italy Legal Entry® est une marque")
        assert (
            str(services.editorial("Écrivez à info@legalitalentry.it", default="Texte par défaut"))
            == "Texte par défaut"
        )


def test_locked_helper_reports_the_effective_language():
    with translation.override("ar"):
        text = services.locked("p3.antifraud.title")
    assert text.value == locked_content.text("p3.antifraud.title", "fr")
    assert text.lang == "fr"
    with translation.override("fr"):
        assert services.locked("p3.antifraud.title").lang == ""


def test_str_source_returns_the_french_msgid_whatever_the_language():
    with translation.override("ar"):
        assert services.str_source(content.HERO_INTERIM["title_fr"]) == (
            "Un écosystème pour les parcours réguliers vers l’Italie"
        )


# ---- interim hero -------------------------------------------------------------------------------
def test_interim_editorial_copy_contains_no_phase3_or_forbidden_wording():
    from cms.forbidden import scan

    # Single common words (« Actualités », « Connexion ») are not prescribed *sentences*: compare real phrases.
    phase3_strings = [
        v
        for k, v in locked_content.LOCKED_TEXTS["fr"].items()
        if k.startswith("p3.") and isinstance(v, str) and len(v) > 25
    ]
    editorial_strings = [services.str_source(v) for v in content.HERO_INTERIM.values()]
    editorial_strings += [services.str_source(x) for e in content.ENTRANCES for x in (e.title, e.text, e.button)]
    editorial_strings += [services.str_source(x) for x in content.ORIENTATION_STEPS + content.TRUST_DOES_NOT]
    editorial_strings += [
        services.str_source(x) for d in content.SECTION_DEFAULTS for x in (d.heading, d.intro, d.note)
    ]
    for value in editorial_strings:
        assert scan(value) == [], value
        for prescribed in phase3_strings:
            assert prescribed.lower() not in value.lower(), (value, prescribed)
            assert not (len(value) > 25 and value.lower() in prescribed.lower()), (value, prescribed)
    assert "doorway" not in " ".join(editorial_strings).lower()


def test_interim_body_reference_is_limited_to_phase1_keys(seeded):
    hero = HomeHero.objects.get(variant=HeroVariant.INTERIM)
    assert hero.body_fr == "locked:p1.persons.replacement_1"  # a reference, never a hand copy
    with translation.override("fr"):
        body, is_locked = services._interim_body(hero.body_fr, "fr")
        assert is_locked and body.value == locked_content.text("p1.persons.replacement_1", "fr")
        # An editor cannot pull a Phase 3 sentence (or an unknown key) into the interim hero.
        assert services._interim_body("locked:p3.hero.body", "fr") == (services.EMPTY, False)
        assert services._interim_body("locked:p9.unknown", "fr") == (services.EMPTY, False)
        assert services._interim_body("locked:p1.companies.form.fields", "fr") == (services.EMPTY, False)
        free_text, is_locked = services._interim_body("Texte libre de l’équipe.", "fr")
        assert (str(free_text), is_locked) == ("Texte libre de l’équipe.", False)


def test_hero_falls_back_to_code_defaults_without_rows(db):
    assert not HomeHero.objects.exists()
    with translation.override("fr"):
        data = services.build_hero(services.BuildContext(request=None, lang="fr", phase3=False))
    assert str(data["title"]) == "Un écosystème pour les parcours réguliers vers l’Italie"
    assert data["primary"]["url"] == "/fr/orientation/"
    assert data["photo"] is None  # no media library yet: a type-led hero, never a broken image


def test_hero_title_never_empty_even_if_an_editor_blanks_it(seeded):
    HomeHero.objects.filter(variant=HeroVariant.INTERIM).update(title_fr="")
    with translation.override("fr"):
        data = services.build_hero(services.BuildContext(request=None, lang="fr", phase3=False))
    assert str(data["title"])


def test_unpublished_interim_hero_row_is_ignored(seeded):
    HomeHero.objects.filter(variant=HeroVariant.INTERIM).update(
        status=PublicationStatus.DRAFT, title_fr="Brouillon non relu"
    )
    with translation.override("fr"):
        data = services.build_hero(services.BuildContext(request=None, lang="fr", phase3=False))
    assert "Brouillon" not in str(data["title"])


def test_cta_is_hidden_when_its_route_does_not_exist():
    with translation.override("fr"):
        assert services._cta("Libellé", "nowhere:missing", "fr") is None
        assert services._cta("", "pages:home", "fr") is None
        assert services._cta("Accueil", "pages:home", "fr")["url"] == "/fr/"


# ---- entrances ----------------------------------------------------------------------------------
@pytest.mark.parametrize("phase3", [False, True])
def test_entrances_are_always_exactly_four_with_a_target(phase3):
    with translation.override("fr"):
        items = services.entrances("fr", phase3)
    assert [item["actor"] for item in items] == ["person", "company", "institution", "university"]
    assert all(item["url"].startswith("/fr/") for item in items)
    assert all(item["illustration"].endswith(".svg") for item in items)
    assert len(content.ENTRANCES) == 4


def test_entrance_texts_come_from_the_registry_only_when_phase3():
    with translation.override("fr"):
        closed = services.entrances("fr", False)
        opened = services.entrances("fr", True)
    assert closed[0]["title"] == "Personnes"
    assert opened[0]["title"] == locked_content.text("p3.entrances.person.title", "fr")
    assert opened[3]["button"] == locked_content.text("p3.entrances.university.button", "fr")


# ---- photographs --------------------------------------------------------------------------------
def test_photo_for_slot_uses_static_derivatives_and_french_alt_fallback(seeded, curated_photo):
    with translation.override("it"):
        photo = services.photo_for_slot("hero")
    assert photo.src == "/static/img/photos/reunion-cooperation-1440.jpg"
    assert "reunion-cooperation-480.webp 480w" in photo.srcset
    assert "reunion-cooperation-1920.webp 1920w" in photo.srcset
    assert photo.alt and photo.alt_lang == "fr"  # no Italian alt supplied yet → French, tagged
    assert (photo.width, photo.height) == (1440, 960)
    with translation.override("fr"):
        assert services.photo_for_slot("hero").alt_lang == ""


def test_photo_helpers_tolerate_missing_assets(db):
    assert services.photo_for_slot("hero") is None
    assert services.photo_from_asset(None) is None
    assert services.photo_from_asset(MediaAsset(title="Sans fichier", alt_fr="x")) is None


def test_every_curated_photo_avoids_forbidden_subjects(seeded):
    from cms.seeds_media import forbidden_keyword_hits

    for slot in ("hero", "workshop", "entrance_institution", "forum_event"):
        asset = services.asset_for_slot(slot)
        assert asset is not None, slot
        assert asset.stereotype_checked
        assert forbidden_keyword_hits(asset.title, asset.alt_fr) == []


# ---- composition --------------------------------------------------------------------------------
def test_section_gate_is_enforced_in_code_for_phase3_sections(seeded):
    row = HomeSection.objects.get(key=SectionKey.ANTIFRAUD)
    row.requires_gate = ""
    assert services.section_gate_open(row, phase3=False) is False
    assert services.section_gate_open(row, phase3=True) is True


def test_unknown_gate_name_closes_the_section(seeded):
    row = HomeSection.objects.get(key=SectionKey.TRUST)
    row.requires_gate = "gate_that_does_not_exist"
    assert services.section_gate_open(row, phase3=True) is False


def test_every_section_key_has_a_builder_a_template_and_a_default():
    from django.template.loader import get_template

    keys = set(SectionKey.values)
    assert set(services.BUILDERS) == keys
    assert {d.key for d in content.SECTION_DEFAULTS} == keys
    for key in keys:
        get_template(f"pages/home/_{key}.html")
    orders = [d.order for d in content.SECTION_DEFAULTS]
    assert orders == sorted(orders)
    assert [d.key for d in content.SECTION_DEFAULTS] == [
        "hero",
        "banner",
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
