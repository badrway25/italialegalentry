"""Sitemap gating and back-office protection of the prescribed rows."""

from __future__ import annotations

import pytest
from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory

from ecosystem.admin import EcosystemSpaceAdmin, PilotStepAdmin
from ecosystem.models import EcosystemSpace, PilotStep, SpaceKey
from ecosystem.sitemaps import EcosystemSitemap

pytestmark = pytest.mark.django_db

GATED_SLUGS = ("/institutions/", "/universites-et-formation/", "/projet-pilote/")


# ---------------------------------------------------------------------------------------------
# Sitemap
# ---------------------------------------------------------------------------------------------
def test_sitemap_is_registered():
    from core.sitemaps import SITEMAPS

    assert SITEMAPS["ecosystem"] is EcosystemSitemap


@pytest.mark.compliance
def test_sitemap_lists_only_the_phase1_page_while_gate_g3_is_closed(client, seeded, before_phase3):
    assert EcosystemSitemap().items() == [SpaceKey.COMPANIES]
    xml = client.get("/sitemap.xml").content.decode("utf-8")
    for lang in ("it", "fr", "en", "ar"):
        assert f"/{lang}/entreprises/</loc>" in xml
    for slug in GATED_SLUGS:
        for lang in ("it", "fr", "en", "ar"):
            assert f"/{lang}{slug}</loc>" not in xml, (lang, slug)


def test_sitemap_lists_the_four_pages_once_phase3_is_public(client, seeded, phase3_open):
    assert EcosystemSitemap().items() == list(SpaceKey.values)
    xml = client.get("/sitemap.xml").content.decode("utf-8")
    for slug in ("/entreprises/", *GATED_SLUGS):
        for lang in ("it", "fr", "en", "ar"):
            assert f"/{lang}{slug}</loc>" in xml, (lang, slug)


def test_sitemap_lastmod_comes_from_the_editorial_row(seeded, phase3_open):
    sitemap = EcosystemSitemap()
    assert sitemap.lastmod(SpaceKey.COMPANIES) == EcosystemSpace.objects.get(key="companies").updated_at
    EcosystemSpace.objects.all().delete()
    assert sitemap.lastmod(SpaceKey.COMPANIES) is None


# ---------------------------------------------------------------------------------------------
# Admin
# ---------------------------------------------------------------------------------------------
@pytest.fixture
def admin_request(superuser):
    request = RequestFactory().get("/backoffice/")
    request.user = superuser
    return request


def test_locked_steps_are_read_only_and_cannot_be_deleted(seeded, admin_request):
    model_admin = PilotStepAdmin(PilotStep, AdminSite())
    locked = PilotStep.objects.get(locked_index=3)
    readonly = model_admin.get_readonly_fields(admin_request, locked)
    for field in ("label_fr", "order", "is_visible", "is_locked", "locked_index"):
        assert field in readonly, field
    assert model_admin.has_delete_permission(admin_request, locked) is False
    assert "delete_selected" not in model_admin.get_actions(admin_request)


def test_additions_are_editable_in_wording(seeded, admin_request):
    model_admin = PilotStepAdmin(PilotStep, AdminSite())
    addition = PilotStep.objects.create(order=9, label_fr="ÉVALUATION PARTAGÉE")
    readonly = model_admin.get_readonly_fields(admin_request, addition)
    assert "label_fr" not in readonly and "order" not in readonly and "is_visible" not in readonly
    assert "is_locked" in readonly, "nobody can lock or unlock a step from the back-office"
    assert model_admin.has_delete_permission(admin_request, addition) is True
    assert "label_fr" not in model_admin.get_readonly_fields(admin_request, None)


def test_space_admin_protects_structure(seeded, admin_request):
    model_admin = EcosystemSpaceAdmin(EcosystemSpace, AdminSite())
    space = EcosystemSpace.objects.get(key="pilot")
    readonly = model_admin.get_readonly_fields(admin_request, space)
    assert "requires_gate" in readonly and "key" in readonly
    assert "intro_note_fr" not in readonly and "hero_image" not in readonly
    assert model_admin.has_delete_permission(admin_request, space) is False
    assert model_admin.has_add_permission(admin_request) is False, "exactly four spaces"
    assert "p3.pilot.sequence" in model_admin.prescribed_texts(space)
    assert model_admin.translation_summary(space)


def test_admin_pages_render(client, seeded, superuser):
    client.force_login(superuser)
    step = PilotStep.objects.get(locked_index=1)
    space = EcosystemSpace.objects.get(key="companies")
    for url in (
        "/backoffice/ecosystem/ecosystemspace/",
        f"/backoffice/ecosystem/ecosystemspace/{space.pk}/change/",
        "/backoffice/ecosystem/pilotstep/",
        f"/backoffice/ecosystem/pilotstep/{step.pk}/change/",
        "/backoffice/ecosystem/pilotstep/add/",
    ):
        assert client.get(url).status_code == 200, url


def test_admin_cannot_rewrite_a_locked_label(client, seeded, superuser):
    client.force_login(superuser)
    step = PilotStep.objects.get(locked_index=1)
    client.post(
        f"/backoffice/ecosystem/pilotstep/{step.pk}/change/",
        {"order": "1", "label_fr": "LIBELLÉ RÉÉCRIT", "is_visible": "on"},
    )
    step.refresh_from_db()
    assert step.label_fr == "BESOINS DES ENTREPRISES"


@pytest.mark.security
def test_back_office_is_denied_by_default(client, seeded, person_user, staff_user):
    """
    Deny by default: an anonymous visitor and a signed-in person are sent to the back-office login,
    and a back-office user whose role carries no ``ecosystem`` permission gets 403 — being
    ``is_staff`` alone never opens the prescribed rows.
    """
    step = PilotStep.objects.get(locked_index=1)
    urls = (
        "/backoffice/ecosystem/ecosystemspace/",
        "/backoffice/ecosystem/pilotstep/",
        f"/backoffice/ecosystem/pilotstep/{step.pk}/change/",
        "/backoffice/ecosystem/pilotstep/add/",
    )
    for url in urls:
        response = client.get(url)
        assert response.status_code == 302 and "login" in response["Location"], url
    client.force_login(person_user)
    for url in urls:
        response = client.get(url)
        assert response.status_code == 302 and "login" in response["Location"], url
    assert not staff_user.has_module_perms("ecosystem"), "precondition: the staff role has no ecosystem permission"
    client.force_login(staff_user)
    for url in urls:
        assert client.get(url).status_code == 403, url
    response = client.post(urls[3], {"order": "9", "label_fr": "ÉTAPE NON AUTORISÉE", "is_visible": "on"})
    assert response.status_code == 403
    assert PilotStep.objects.count() == 8
