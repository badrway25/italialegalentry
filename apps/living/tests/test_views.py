import datetime as dt

import pytest
from django.contrib.sitemaps.views import sitemap
from django.test import Client

from cms import locked_content
from cms.models import PublicationStatus
from living.sitemaps import LivingSitemap

pytestmark = pytest.mark.django_db

INDEX = "/fr/vivre-en-italie/"


def test_gate_closed_returns_404_everywhere(client, topics, sheet_factory, before_phase3):
    sheet_factory("S", slug="s")
    assert client.get(INDEX).status_code == 404
    assert client.get(INDEX + "logement/").status_code == 404
    assert client.get(INDEX + "logement/s/").status_code == 404


def test_gate_closed_without_flag_even_after_date(client, topics):
    from freezegun import freeze_time

    with freeze_time("2026-10-10 10:00:00"):
        assert client.get(INDEX).status_code == 404


def test_index_lists_seeded_topics_with_locked_intro(client, topics, phase3_open):
    r = client.get(INDEX)
    assert r.status_code == 200
    html = r.content.decode()
    assert html.count("<h1") == 1
    assert locked_content.text("p3.living.title", "fr") in html
    assert locked_content.text("p3.living.body", "fr") in html
    for label in ("Langue italienne", "Logement", "Santé", "École", "Services publics", "Fiscalité de base"):
        assert label in html
    assert html.count("Fiches en préparation") == 10
    assert 'href="/fr/vivre-en-italie/logement/"' in html


def test_index_counts_live_sheets(client, topics, sheet_factory, phase3_open):
    sheet_factory("A", slug="a")
    sheet_factory("B", slug="b")
    sheet_factory("Draft", slug="d", status=PublicationStatus.DRAFT)
    html = client.get(INDEX).content.decode()
    assert "2 fiches" in html
    assert html.count("Fiches en préparation") == 9


def test_topic_page_empty_state_and_listing(client, topics, sheet_factory, phase3_open):
    r = client.get(INDEX + "logement/")
    assert r.status_code == 200
    html = r.content.decode()
    assert html.count("<h1") == 1 and "Logement" in html
    assert "Fiches en préparation" in html
    assert "en cours de rédaction et de vérification" in html
    sheet_factory("Trouver un logement", slug="trouver", last_reviewed_at=dt.datetime(2026, 10, 3, tzinfo=dt.UTC))
    sheet_factory("Brouillon", slug="brouillon", status=PublicationStatus.DRAFT)
    html = client.get(INDEX + "logement/").content.decode()
    assert "Trouver un logement" in html and "Brouillon" not in html
    assert "Fiches en préparation" not in html
    assert "03.10.2026" in html
    assert client.get(INDEX + "inconnu/").status_code == 404


def test_unpublished_topic_404(client, topics, phase3_open):
    from living.models import LivingTopic

    LivingTopic.objects.filter(slug="ecole").update(status=PublicationStatus.DRAFT)
    assert client.get(INDEX + "ecole/").status_code == 404


def test_sheet_detail_metadata_sources_and_404s(client, topics, sheet_factory, phase3_open):
    sheet = sheet_factory(
        "Inscription au SSN",
        slug="inscription",
        last_reviewed_at=dt.datetime(2026, 10, 3, 9, 0, tzinfo=dt.UTC),
        sources=[{"label": "Ministero della Salute", "url": "https://www.salute.gov.it/"}],
    )
    r = client.get(sheet.get_absolute_url())
    assert r.status_code == 200
    html = r.content.decode()
    assert html.count("<h1") == 1 and "Inscription au SSN" in html
    assert "Dernière vérification" in html and "03.10.2026" in html
    assert 'href="https://www.salute.gov.it/" rel="noopener noreferrer external"' in html
    assert "<h2>Section</h2>" in html and "<li>a</li>" in html
    assert "ne remplacent pas les indications des autorités compétentes" in html
    assert 'aria-current="page"' in html
    assert client.get(INDEX + "sante/inscription/").status_code == 404, "sheet belongs to another topic"
    draft = sheet_factory("Draft", slug="draft", status=PublicationStatus.DRAFT)
    assert client.get(draft.get_absolute_url()).status_code == 404
    unreviewed = sheet_factory("Unrev", slug="unrev", status=PublicationStatus.DRAFT, reviewed=False)
    assert client.get(unreviewed.get_absolute_url()).status_code == 404


def test_staff_preview_before_gate(client, topics, before_phase3, staff_user, person_user):
    from accounts.roles import ensure_roles

    ensure_roles()
    client.force_login(person_user)
    assert client.get(INDEX + "?preview=1").status_code == 404
    client.force_login(staff_user)
    assert client.get(INDEX).status_code == 404, "preview must be explicit"
    r = client.get(INDEX + "?preview=1")
    assert r.status_code == 200
    html = r.content.decode()
    assert 'name="robots" content="noindex' in html
    assert "Aperçu réservé à la rédaction" in html
    assert client.get(INDEX + "logement/?preview=1").status_code == 200


def test_rtl_and_all_languages(client_ar, topics, sheet_factory, phase3_open):
    sheet = sheet_factory("Fiche", slug="fiche")
    r = client_ar.get("/ar/vivre-en-italie/")
    assert r.status_code == 200
    html = r.content.decode()
    assert '<html lang="ar" dir="rtl"' in html
    assert 'lang="fr"' in html, "locked texts fall back to French with lang attribute"
    for lang in ("it", "fr", "en", "ar"):
        assert Client().get(f"/{lang}/vivre-en-italie/logement/").status_code == 200
        assert Client().get(f"/{lang}/vivre-en-italie/logement/{sheet.slug}/").status_code == 200


def test_post_not_allowed(client, topics, phase3_open):
    assert client.post(INDEX).status_code == 405


def test_sitemap_empty_before_gate_and_complete_after(rf, topics, sheet_factory, before_phase3, set_flag):
    sheet_factory("S", slug="s")
    assert LivingSitemap().items() == []
    from freezegun import freeze_time

    from core import flags

    with freeze_time("2026-10-03 10:00:00"):
        flags.invalidate()
        items = LivingSitemap().items()
        assert len(items) == 1 + 10 + 1
        request = rf.get("/sitemap.xml")
        response = sitemap(request, sitemaps={"living": LivingSitemap})
        response.render()
        xml = response.content.decode()
        assert "/fr/vivre-en-italie/</loc>" in xml
        assert "/ar/vivre-en-italie/logement/s/" in xml


def test_public_routes_registered_as_gated():
    from core.public_routes import all_routes

    living = [r for r in all_routes() if r.app == "living"]
    assert living and all(r.requires_gate == "phase3_public" for r in living)
    assert any(r.path == "vivre-en-italie/" for r in living)
    assert any(r.path == "vivre-en-italie/langue-italienne/" for r in living)
