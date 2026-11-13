"""
Second independent review — adversarial probes that the builder's and the first reviewer's suites
did not cover: back-office access control, forbidden wording in translation rows, prescribed text
pasted by an editor into an editorial field, preview responses, query budget in every state.
"""

from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError

from cms.models import HeroVariant, HomeHero, TranslationStatus
from pages.models import HomeSection, HomeSectionTranslation, SectionKey
from pages.tests.conftest import LANGS, escaped, text_of

pytestmark = pytest.mark.django_db

ADMIN = "/backoffice/pages/homesection/"


# ---- back-office access ---------------------------------------------------------------------------
@pytest.mark.security
def test_backoffice_sections_are_closed_to_anonymous_and_front_office_users(client, seeded, person_user):
    response = client.get(ADMIN)
    assert response.status_code == 302 and "login" in response["Location"]
    client.force_login(person_user)
    response = client.get(ADMIN)
    assert response.status_code in (302, 403)
    assert b"form-0-order" not in response.content


@pytest.mark.security
def test_staff_without_model_permission_cannot_read_or_change_sections(client, seeded, user_factory):
    bare = user_factory("bare-staff@example.test", is_staff=True)
    client.force_login(bare)
    section = HomeSection.objects.get(key=SectionKey.TRUST)
    before = section.heading_fr
    assert client.get(ADMIN).status_code == 403
    assert client.get(f"{ADMIN}{section.pk}/change/").status_code == 403
    assert client.post(f"{ADMIN}{section.pk}/change/", {"heading_fr": "Pris en otage"}).status_code == 403
    section.refresh_from_db()
    assert section.heading_fr == before


@pytest.mark.security
def test_sections_can_never_be_deleted_even_by_a_superuser(client, seeded, superuser):
    client.force_login(superuser)
    section = HomeSection.objects.get(key=SectionKey.TRUST)
    assert client.post(f"{ADMIN}{section.pk}/delete/", {"post": "yes"}).status_code == 403
    assert HomeSection.objects.filter(pk=section.pk).exists()


# ---- translation rows -----------------------------------------------------------------------------
@pytest.mark.compliance
def test_translation_row_with_forbidden_wording_is_rejected_and_never_rendered(client, seeded):
    section = HomeSection.objects.get(key=SectionKey.TRUST)
    row = HomeSectionTranslation(
        master=section,
        language="en",
        heading="Our matching service",
        intro="Italy Legal Entry® informs",
        status=TranslationStatus.PUBLISHED,
    )
    with pytest.raises(ValidationError) as excinfo:
        row.full_clean()
    assert {"heading", "intro"} <= set(excinfo.value.message_dict)
    row.save()  # a row written around the form (import, shell) is still filtered at render time
    html = client.get("/en/").content.decode()
    assert "matching" not in html.lower()
    assert "®" not in html


# ---- prescribed wording pasted into an editorial field --------------------------------------------
@pytest.mark.compliance
def test_editor_cannot_store_a_prescribed_sentence_in_an_editorial_field(seeded):
    section = HomeSection.objects.get(key=SectionKey.TRUST)
    section.intro_fr = f"En bref : {text_of('p3.hero.body')}"
    with pytest.raises(ValidationError) as excinfo:
        section.full_clean()
    assert "intro_fr" in excinfo.value.message_dict
    section.intro_fr = "Une introduction rédigée par l’équipe, sans texte prescrit."
    section.full_clean()


@pytest.mark.compliance
@pytest.mark.parametrize("lang", LANGS)
def test_phase3_sentence_pasted_by_an_editor_is_not_published_while_gate_closed(client, seeded, lang):
    """The gate must hold even when Phase 3 wording reaches an editorial column (section or hero)."""
    HomeSection.objects.filter(key=SectionKey.TRUST).update(intro_fr=text_of("p3.hero.body"))
    HomeSection.objects.filter(key=SectionKey.ENTRANCES).update(heading_fr=text_of("p3.hero.subtitle"))
    HomeHero.objects.filter(variant=HeroVariant.INTERIM).update(
        subtitle_fr=text_of("p3.hero.subtitle"), body_fr=text_of("p3.antifraud.body")
    )
    html = client.get(f"/{lang}/").content.decode()
    for key in ("p3.hero.body", "p3.hero.subtitle", "p3.antifraud.body"):
        assert escaped(text_of(key)) not in html, key
    assert html.count("<h1") == 1


@pytest.mark.compliance
def test_already_public_prescribed_wording_is_not_blocked_by_the_phase3_filter(client, seeded):
    """Only Phase 3 wording is gated: an editorial sentence of the team is rendered as written."""
    HomeSection.objects.filter(key=SectionKey.TRUST).update(intro_fr="Une plateforme d’information et d’orientation.")
    html = client.get("/fr/").content.decode()
    assert "Une plateforme d’information et d’orientation." in html


# ---- preview --------------------------------------------------------------------------------------
@pytest.mark.security
def test_staff_preview_is_never_cacheable_by_a_shared_cache(client, seeded, staff_user):
    client.force_login(staff_user)
    response = client.get("/fr/attention-aux-fraudes/?preview=1")
    assert response.status_code == 200
    cache_control = response.get("Cache-Control", "")
    assert "private" in cache_control or "no-store" in cache_control


# ---- query budget in every state ------------------------------------------------------------------
@pytest.mark.parametrize("lang", LANGS)
def test_homepage_query_budget_in_every_language_phase3_open(
    client, seeded, phase3_open, lang, django_assert_max_num_queries
):
    client.get(f"/{lang}/")
    with django_assert_max_num_queries(40):
        client.get(f"/{lang}/")


# ---- prescribed-wording detector ------------------------------------------------------------------
def test_prescribed_detector_separates_phase3_from_already_public_wording():
    from pages import prescribed

    assert prescribed.phase3_only(text_of("p3.hero.body"))
    assert prescribed.phase3_only(f"Avant-propos. {text_of('p3.antifraud.body')} Fin.")
    assert not prescribed.phase3_only(text_of("p2.forum.why.body"))
    assert not prescribed.phase3_only(text_of("p1.persons.replacement_1"))
    assert prescribed.any_phase(text_of("p2.forum.why.body"))
    assert prescribed.any_phase(text_of("p1.persons.replacement_1"))
    assert not prescribed.any_phase("")
    assert not prescribed.any_phase("Une introduction rédigée par l’équipe, sans texte prescrit.")
    # Typographic variants of the same sentence are still recognised (case, apostrophes, spacing).
    assert prescribed.phase3_only(text_of("p3.hero.body").upper().replace("’", "'").replace(" ", "  "))


def test_every_seeded_editorial_default_passes_the_detector():
    from pages import content, prescribed, services

    values = [services.str_source(v) for d in content.SECTION_DEFAULTS for v in (d.heading, d.intro, d.note)]
    values += [services.str_source(v) for v in content.HERO_INTERIM.values()]
    values += [services.str_source(v) for v in content.TRUST_DOES_NOT + content.ORIENTATION_STEPS]
    values += [services.str_source(v) for a in content.NETWORK_ACTORS for v in (a.title, a.text, a.link_label)]
    values += [services.str_source(v) for e in content.ENTRANCES for v in (e.title, e.text, e.button)]
    for value in filter(None, values):
        assert not prescribed.any_phase(value), value


def test_admin_form_refuses_prescribed_text_without_crashing_on_read_only_headings(seeded, superuser):
    """Pilot has a prescribed (read-only) heading: the error must land on a field the form really has."""
    from django.contrib.admin.sites import AdminSite
    from django.forms.models import model_to_dict
    from django.test import RequestFactory

    from pages.admin import HomeSectionAdmin

    request = RequestFactory().get(ADMIN)
    request.user = superuser
    section = HomeSection.objects.get(key=SectionKey.PILOT)
    # A value written around the form into a column this section never renders must not break the form.
    HomeSection.objects.filter(pk=section.pk).update(heading_fr=text_of("p3.hero.subtitle"))
    section.refresh_from_db()
    form_class = HomeSectionAdmin(HomeSection, AdminSite()).get_form(request, section)
    data = {name: ("" if value is None else value) for name, value in model_to_dict(section).items()}
    data["intro_fr"] = text_of("p3.hero.body")
    form = form_class(data=data, instance=section)
    assert not form.is_valid()
    assert "intro_fr" in form.errors and "heading_fr" not in form.errors
    data["intro_fr"] = "Une introduction rédigée par l’équipe."
    assert form_class(data=data, instance=HomeSection.objects.get(pk=section.pk)).is_valid()
