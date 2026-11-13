"""HomeSection model, idempotent seeds and the back-office (ordering without drag and drop, locked fields)."""

from __future__ import annotations

import pytest
from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import RequestFactory

from cms.models import HeroVariant, HomeHero, PublicationStatus, TranslationStatus
from pages import content, seeds
from pages.admin import HomeSectionAdmin
from pages.models import (
    LOCKED_KEYS_BY_SECTION,
    HomeSection,
    HomeSectionTranslation,
    SectionKey,
)

pytestmark = pytest.mark.django_db


# ---- model --------------------------------------------------------------------------------------
def test_section_key_is_unique(seeded):
    with pytest.raises(IntegrityError), transaction.atomic():
        HomeSection.objects.create(key=SectionKey.HERO, order=999)


def test_translation_is_unique_per_language(seeded):
    section = HomeSection.objects.get(key=SectionKey.TRUST)
    HomeSectionTranslation.objects.create(master=section, language="it", heading="Uno")
    with pytest.raises(IntegrityError), transaction.atomic():
        HomeSectionTranslation.objects.create(master=section, language="it", heading="Due")


def test_visible_queryset_filters_status_activation_and_orders(seeded):
    HomeSection.objects.filter(key=SectionKey.NEWS).update(is_enabled=False)
    HomeSection.objects.filter(key=SectionKey.TRUST).update(status=PublicationStatus.ARCHIVED)
    HomeSection.objects.filter(key=SectionKey.ECOSYSTEM).update(order=5)
    keys = list(HomeSection.objects.visible().values_list("key", flat=True))
    assert keys[0] == "ecosystem"
    assert "news" not in keys and "trust" not in keys
    assert len(keys) == 9


def test_clean_rejects_forbidden_formulations(seeded):
    section = HomeSection.objects.get(key=SectionKey.TRUST)
    section.intro_fr = "Notre service de matching"
    with pytest.raises(ValidationError) as excinfo:
        section.full_clean()
    assert "intro_fr" in excinfo.value.message_dict
    section.intro_fr = "Italy Legal Entry® informe"
    with pytest.raises(ValidationError):
        section.full_clean()
    section.intro_fr = "Italy Legal Entry™ informe et oriente."
    section.full_clean()


def test_locked_key_map_only_references_existing_registry_keys():
    from cms import locked_content

    assert set(LOCKED_KEYS_BY_SECTION) == set(SectionKey.values)
    known = set(locked_content.keys())
    for section, keys in LOCKED_KEYS_BY_SECTION.items():
        assert set(keys) <= known, section


def test_no_prescribed_text_is_stored_in_the_database(seeded):
    """Prescribed sentences live in the registry only: rows hold editorial strings or references."""
    from cms import locked_content

    prescribed = [v for v in locked_content.LOCKED_TEXTS["fr"].values() if isinstance(v, str) and len(v) > 25]
    stored = []
    for section in HomeSection.objects.all():
        stored += [section.heading_fr, section.intro_fr, section.note_fr]
    for hero in HomeHero.objects.all():
        stored += [hero.eyebrow_fr, hero.title_fr, hero.subtitle_fr, hero.body_fr]
    for value in filter(None, stored):
        for sentence in prescribed:
            assert sentence not in value, value


# ---- seeds --------------------------------------------------------------------------------------
def test_seed_creates_eleven_sections_in_the_prescribed_order(seeded):
    rows = list(HomeSection.objects.ordered())
    assert [r.key for r in rows] == [d.key for d in content.SECTION_DEFAULTS]
    assert len(rows) == 11
    assert all(r.status == PublicationStatus.PUBLISHED and r.is_enabled for r in rows)
    gates = {r.key: r.requires_gate for r in rows}
    assert gates["banner"] == "forum_banner"
    assert gates["pilot"] == gates["antifraud"] == gates["reserved"] == "phase3_public"
    assert gates["hero"] == gates["entrances"] == gates["trust"] == ""


def test_seed_hero_variants(seeded):
    interim = HomeHero.objects.get(variant=HeroVariant.INTERIM)
    phase3 = HomeHero.objects.get(variant=HeroVariant.PHASE3)
    assert interim.status == PublicationStatus.PUBLISHED
    assert interim.title_fr == "Un écosystème pour les parcours réguliers vers l’Italie"
    assert interim.primary_cta_url_name == "orientation:start"
    assert interim.secondary_cta_url_name == "enquiries:company_needs"
    assert interim.image is not None and "slot=hero;" in interim.image.license_notes
    # The Phase 3 row stores no text (p3.hero.* come from the registry) and is date-scheduled.
    assert (phase3.title_fr, phase3.subtitle_fr, phase3.body_fr) == ("", "", "")
    assert phase3.status == PublicationStatus.SCHEDULED
    assert phase3.publish_at.date().isoformat() in {"2026-10-01", "2026-10-02"}  # 2 Oct 00:00 Europe/Rome


def test_seeds_are_idempotent_and_never_overwrite_editorial_changes(seeded):
    HomeSection.objects.filter(key=SectionKey.TRUST).update(
        heading_fr="Titre choisi par la rédaction", order=15, is_enabled=False, requires_gate="newsletter"
    )
    HomeHero.objects.filter(variant=HeroVariant.INTERIM).update(title_fr="Titre éditorial modifié", image=None)
    seeds.seed_home_sections()
    seeds.seed_home_hero()
    seeds.seed_home_sections()
    assert HomeSection.objects.count() == 11
    assert HomeHero.objects.count() == 2
    section = HomeSection.objects.get(key=SectionKey.TRUST)
    assert (section.heading_fr, section.order, section.is_enabled, section.requires_gate) == (
        "Titre choisi par la rédaction",
        15,
        False,
        "newsletter",
    )
    hero = HomeHero.objects.get(variant=HeroVariant.INTERIM)
    assert hero.title_fr == "Titre éditorial modifié"
    assert hero.image is not None  # only a missing photo is filled in


# ---- admin --------------------------------------------------------------------------------------
@pytest.fixture
def section_admin():
    return HomeSectionAdmin(HomeSection, AdminSite())


@pytest.fixture
def admin_request(superuser):
    request = RequestFactory().get("/backoffice/pages/homesection/")
    request.user = superuser
    return request


def test_admin_orders_without_drag_and_drop(section_admin):
    assert "order" in section_admin.list_editable and "is_enabled" in section_admin.list_editable
    assert section_admin.ordering == ("order", "id")
    assert "gate_state" in section_admin.list_display


def test_admin_locks_prescribed_fields(section_admin, admin_request, seeded):
    hero = HomeSection.objects.get(key=SectionKey.HERO)
    pilot = HomeSection.objects.get(key=SectionKey.PILOT)
    trust = HomeSection.objects.get(key=SectionKey.TRUST)
    hero_ro = section_admin.get_readonly_fields(admin_request, hero)
    assert {"key", "heading_fr", "intro_fr", "note_fr", "locked_texts", "version", "published_at"} <= set(hero_ro)
    pilot_ro = section_admin.get_readonly_fields(admin_request, pilot)
    assert "heading_fr" in pilot_ro and "intro_fr" not in pilot_ro
    trust_ro = section_admin.get_readonly_fields(admin_request, trust)
    assert "heading_fr" not in trust_ro and "key" in trust_ro
    assert "key" not in section_admin.get_readonly_fields(admin_request, None)


def test_admin_shows_locked_keys_and_gate_state(section_admin, seeded):
    antifraud = HomeSection.objects.get(key=SectionKey.ANTIFRAUD)
    html = str(section_admin.locked_texts(antifraud))
    assert "p3.antifraud.title" in html and "p3.antifraud.body" in html
    assert section_admin.gate_state(antifraud) is False
    assert section_admin.gate_state(HomeSection.objects.get(key=SectionKey.TRUST)) is True
    assert section_admin.has_delete_permission(None) is False


def test_admin_changelist_and_change_form_render(client, superuser, seeded):
    client.force_login(superuser)
    response = client.get("/backoffice/pages/homesection/")
    assert response.status_code == 200
    html = response.content.decode()
    assert 'name="form-0-order"' in html and 'name="form-0-is_enabled"' in html
    section = HomeSection.objects.get(key=SectionKey.ANTIFRAUD)
    response = client.get(f"/backoffice/pages/homesection/{section.pk}/change/")
    assert response.status_code == 200
    form_html = response.content.decode()
    assert "p3.antifraud.body" in form_html
    assert 'name="heading_fr"' not in form_html  # prescribed heading: read-only
    assert 'name="intro_fr"' in form_html


def test_admin_reorder_through_the_list_changes_the_homepage(before_the_forum, client, superuser, seeded):
    # The expected order includes the Forum banner, which is up only until 2 Oct 2026 00:00 Rome.
    client.force_login(superuser)
    rows = list(HomeSection.objects.ordered())
    data = {
        "form-TOTAL_FORMS": str(len(rows)),
        "form-INITIAL_FORMS": str(len(rows)),
        "form-MIN_NUM_FORMS": "0",
        "form-MAX_NUM_FORMS": "1000",
        "_save": "Save",
    }
    for index, row in enumerate(rows):
        data[f"form-{index}-id"] = str(row.pk)
        data[f"form-{index}-order"] = "35" if row.key == "ecosystem" else str(row.order)
        if row.is_enabled and row.key != "orientation":
            data[f"form-{index}-is_enabled"] = "on"
    response = client.post("/backoffice/pages/homesection/", data)
    assert response.status_code == 302
    client.logout()
    html = client.get("/fr/").content.decode()
    import re

    order = re.findall(r'data-section="([a-z]+)"', html)
    assert order == ["hero", "banner", "entrances", "ecosystem", "pathways", "trust"]


def test_translation_inline_defaults_to_draft(seeded):
    section = HomeSection.objects.get(key=SectionKey.TRUST)
    row = HomeSectionTranslation.objects.create(master=section, language="en", heading="What the platform does")
    assert row.status == TranslationStatus.DRAFT and not row.is_public
