"""Integration tests of the reserved-area pages (real rows, empty states, pagination, i18n/RTL, a11y)."""

from __future__ import annotations

import re

import pytest
from django.utils import timezone

from core.models import SiteSettings
from portal.tests.conftest import DASHBOARD, DEADLINES, DOCUMENTS, MESSAGES, PATHWAYS, REQUESTS

pytestmark = pytest.mark.django_db

ALL_PAGES = [DASHBOARD, REQUESTS, PATHWAYS, DOCUMENTS, DEADLINES, MESSAGES]


def _html(client, path, status=200):
    response = client.get(path)
    assert response.status_code == status, (path, response.status_code)
    return response.content.decode("utf-8")


def _card(html: str, key: str) -> str:
    # a register of the bridge (design V5, W3-B step 2: templates/portal/partials/card.html), by its key
    match = re.search(rf'<section class="db-card"[^>]*data-card="{key}".*?</section>', html, flags=re.S)
    assert match, f"card {key} not rendered"
    return match.group(0)


# ---- dashboard ------------------------------------------------------------------------------
def test_dashboard_for_a_fresh_account_shows_empty_states_not_numbers(client, seeded, alice):
    """
    An empty region is one hairline and one sentence naming who fills it and when, with the
    resolving action inline — never a dashed box with a centred icon, and never a zero.

    Rewritten on 21/09/2026 with the Person dashboard: the five equally-weighted cards, four of them
    empty, are gone. The two principles they guarded are kept: an empty region prints no figure, and
    a region with content prints the real one (the test below).
    """
    client.force_login(alice)
    html = _html(client, DASHBOARD)
    assert 'class="portal-cards"' not in html, "the Person dashboard is not a card grid"
    assert 'class="empty-state"' not in html, "no dashed box with a centred icon"
    # design V5 (W3-B): an empty region is one line, `db-empty` — the dates, the communications, the Academy
    assert html.count('class="db-empty"') >= 3
    assert "data-count" not in html, "an empty region must not print a figure"
    assert 'data-card="organisation"' not in html
    assert "Alice ALPHA-UNIQUE" in html and alice.email in html


def test_dashboard_cards_show_the_real_counts(
    client, seeded, alice, make_contact_request, make_document, make_message, make_deadline, completed_orientation
):
    for i in range(4):
        make_contact_request(alice, subject=f"Sujet numéro {i}", message=f"Texte {i}")
    make_document(alice, name="contrat-alice.pdf")
    make_message(alice, subject="Convocation Alice")
    make_message(alice, subject="Rappel Alice")
    make_deadline(alice, title="Dépôt Alice", days=3)
    completed_orientation(alice)
    client.force_login(alice)
    html = _html(client, DASHBOARD)
    assert "contrat-alice.pdf" in html
    assert "Convocation Alice" in html and "Rappel Alice" in html
    assert "Dépôt Alice" in html
    # Real rows, in real lists: no empty state is drawn where there is content (design V5, W3-B: the
    # dashboard's dates and communications are the rows of its flat lists, `db-list__row`).
    assert html.count('class="db-list__row') >= 3 and 'class="db-list__row db-list__row--unread"' in html
    assert "Dépôt Alice" in html
    # The pre-assessment is shown with its ruleset version and its evaluation date, because an
    # outcome without them cannot be reproduced and should not be trusted.
    assert "Votre pré-évaluation" in html


def test_dashboard_links_profile_security_and_account_menu(client, seeded, alice):
    client.force_login(alice)
    html = _html(client, DASHBOARD)
    assert 'href="/fr/compte/profil/"' in html
    assert 'href="/fr/compte/2fa/"' in html
    assert 'class="account-menu"' in html, "design-system account menu (utility bar)"
    assert "/backoffice/" not in html


def test_staff_account_gets_the_backoffice_link(client, seeded, staff_user):
    client.force_login(staff_user)
    assert 'href="/backoffice/"' in _html(client, DASHBOARD)


def test_company_account_sees_its_organisation_card(client, seeded, company_a):
    user, organisation = company_a
    client.force_login(user)
    card = _card(_html(client, DASHBOARD), "organisation")
    assert organisation.name in card and "Rovigo" in card


def test_published_notice_is_shown_inside_the_portal_only(client, seeded, alice):
    from cms.models import PublicationStatus
    from portal.models import PortalNotice

    PortalNotice.objects.create(
        audience="person",
        heading_fr="Avis aux personnes",
        body_fr="Ligne 1\nLigne 2",
        status=PublicationStatus.PUBLISHED,
    )
    PortalNotice.objects.create(audience="company", heading_fr="Avis entreprises", body_fr="x", status="published")
    client.force_login(alice)
    html = _html(client, DASHBOARD)
    assert "Avis aux personnes" in html and "Ligne 1<br>Ligne 2" in html
    assert "Avis entreprises" not in html
    client.logout()
    assert "Avis aux personnes" not in client.get("/fr/").content.decode()


# ---- requests -------------------------------------------------------------------------------
def test_requests_list_is_paginated(client, seeded, alice, make_contact_request):
    for i in range(23):
        make_contact_request(alice, subject=f"Demande {i:02d}", message=f"Corps {i}")
    client.force_login(alice)
    first = _html(client, REQUESTS)
    # one row a request (design V5, W3-E: the register's rows, `data-request` — the table V4 drew is gone)
    assert first.count('data-request="') == 10
    assert 'class="pagination"' in first and "Page 1 sur 3" in first and 'rel="next"' in first
    assert "Demande 22" in first and "Demande 00" not in first, "newest first"
    last = _html(client, REQUESTS + "?page=3")
    assert last.count('data-request="') == 3 and "Demande 00" in last and 'rel="prev"' in last
    assert "Page 3 sur 3" in _html(client, REQUESTS + "?page=999")
    assert "Page 1 sur 3" in _html(client, REQUESTS + "?page=abc")


def test_requests_empty_state(client, seeded, alice):
    client.force_login(alice)
    html = _html(client, REQUESTS)
    assert 'class="empty-state"' in html and "<table" not in html


def test_request_detail_shows_own_data_and_consent_metadata(client, seeded, alice, make_company_request):
    obj = make_company_request(alice, company_name="Atelier Alpha", profiles_needed="Soudeurs qualifiés")
    obj.admin_notes = "NOTE-INTERNE-SECRETE"
    obj.ip_hash = "deadbeefdeadbeef"
    obj.save()
    client.force_login(alice)
    html = _html(client, f"{REQUESTS}besoins-entreprise/{obj.pk}/")
    assert "Atelier Alpha" in html and "Soudeurs qualifiés" in html
    assert "Votre consentement" in html
    assert f"v{obj.consent.consent_text.version}" in html
    # The page shows the date in Rome, as the ``date`` filter renders it; ``given_at`` is held in UTC,
    # whose date is the day before between 00:00 and 02:00 in Rome.
    assert timezone.localtime(obj.consent.given_at).strftime("%d.%m.%Y") in html
    assert "NOTE-INTERNE-SECRETE" not in html and "deadbeefdeadbeef" not in html


def test_request_detail_dates_are_rome_dates_after_midnight(
    after_midnight_in_rome, client, seeded, alice, make_company_request
):
    """At 00:30 in Rome a request sent «today» shows today's date — not the UTC date, still yesterday."""
    obj = make_company_request(alice, company_name="Atelier Minuit")
    assert obj.consent.given_at.date().isoformat() == "2026-10-04", "held in UTC: the trap"
    client.force_login(alice)
    html = _html(client, f"{REQUESTS}besoins-entreprise/{obj.pk}/")
    assert "05.10.2026 00:30" in html, "sent and consented at 00:30 on 5 October, Rome time"
    assert "04.10.2026" not in html


def test_request_detail_unknown_kind_or_pk_is_404(client, seeded, alice):
    client.force_login(alice)
    assert client.get(f"{REQUESTS}contact/987654/").status_code == 404
    assert client.get(f"{REQUESTS}inconnu/1/").status_code == 404


# ---- pathways -------------------------------------------------------------------------------
def test_pathways_lists_results_with_version_date_outcome_checklist_and_notice(client, alice, completed_orientation):
    _session, result = completed_orientation(alice)
    client.force_login(alice)
    html = _html(client, PATHWAYS)
    assert 'data-result-kind="informational"' in html
    assert "Pré-évaluation à caractère informatif" in html
    assert "Il ne constitue pas une décision" in html
    assert result.outcome.title_fr in html
    assert f"v{result.ruleset_version}" in html
    assert timezone.localtime(result.created_at).strftime("%d.%m.%Y") in html  # Rome's date, as rendered
    first_item = result.outcome.checklist_items.order_by("category", "order", "id").first()
    if first_item is not None:
        assert first_item.text_fr in html
    assert 'href="/fr/orientation/"' in html, "link to restart the orientation"
    assert f"/fr/orientation/session/{result.session_id}/resultat/" in html


def test_pathways_result_date_is_the_rome_date_after_midnight(
    after_midnight_in_rome, client, alice, completed_orientation
):
    """The result of a questionnaire finished at 00:30 in Rome is dated that day in the list."""
    _session, result = completed_orientation(alice)
    assert result.created_at.date().isoformat() == "2026-10-04", "held in UTC: the trap"
    client.force_login(alice)
    html = _html(client, PATHWAYS)
    assert '<time datetime="2026-10-05T00:30:00+02:00">05.10.2026</time>' in html
    assert "04.10.2026" not in html


def test_pathways_empty_state_links_to_orientation_start(client, seeded, alice):
    client.force_login(alice)
    html = _html(client, PATHWAYS)
    assert 'class="empty-state"' in html and 'href="/fr/orientation/"' in html


def test_pathways_renders_the_locked_disclaimer_from_the_registry(client, alice, completed_orientation):
    from cms import locked_content

    completed_orientation(alice)
    client.force_login(alice)
    html = _html(client, PATHWAYS)
    expected = locked_content.text("p3.persons.how_it_works", "fr")
    from django.utils.html import escape

    assert escape(expected) in html


# ---- documents ------------------------------------------------------------------------------
def test_documents_page_links_download_and_upload(client, seeded, alice, make_document):
    doc = make_document(alice, name="diplome-alice.pdf")
    client.force_login(alice)
    html = _html(client, DOCUMENTS)
    assert f'href="/documents/{doc.pk}/"' in html
    assert 'href="/documents/upload/"' in html
    assert "diplome-alice.pdf" in html


def test_documents_upload_entry_point_requires_accepted_terms(client, seeded, user_factory):
    user = user_factory("noterms@example.test")
    client.force_login(user)
    html = _html(client, DOCUMENTS)
    assert 'href="/documents/upload/"' not in html
    assert 'class="notice notice--pending"' in html


# ---- deadlines / messages -------------------------------------------------------------------
def test_deadlines_page_separates_open_and_closed(client, seeded, alice, make_deadline):
    make_deadline(alice, title="Échéance ouverte", days=2, source_note="Courrier du 12.09.2026")
    make_deadline(alice, title="Échéance passée", days=-3)
    make_deadline(alice, title="Échéance close", days=-10, status="done")
    client.force_login(alice)
    html = _html(client, DEADLINES)
    assert "Échéance ouverte" in html and "Courrier du 12.09.2026" in html
    assert "En retard" in html and "Bientôt" in html
    assert html.index("Échéance ouverte") < html.index("Échéance close")


def test_messages_inbox_detail_and_mark_as_read(client, seeded, alice, make_message):
    message = make_message(alice, subject="Convocation", body="Première ligne\n\nSeconde <b>ligne</b>")
    client.force_login(alice)
    inbox = _html(client, MESSAGES)
    assert "Convocation" in inbox and "Non lue" in inbox and 'data-unread="1"' in inbox
    detail = _html(client, f"{MESSAGES}{message.pk}/")
    assert "<p>Première ligne</p>" in detail
    assert "&lt;b&gt;ligne&lt;/b&gt;" in detail, "message bodies are plain text, always escaped"
    message.refresh_from_db()
    assert message.is_read is False, "a GET never changes state"
    response = client.post(f"{MESSAGES}{message.pk}/lu/")
    assert response.status_code == 302 and response["Location"].endswith(f"{message.pk}/")
    message.refresh_from_db()
    assert message.is_read is True and message.read_at is not None
    assert "Toutes vos communications sont lues." in _html(client, MESSAGES)


def test_mark_as_read_from_the_list_returns_to_the_list_and_ignores_free_urls(client, seeded, alice, make_message):
    message = make_message(alice)
    client.force_login(alice)
    response = client.post(f"{MESSAGES}{message.pk}/lu/", {"next": "list"})
    assert response["Location"] == MESSAGES
    other = make_message(alice)
    response = client.post(f"{MESSAGES}{other.pk}/lu/", {"next": "https://evil.example/"})
    assert response["Location"].startswith(MESSAGES) and "evil" not in response["Location"]


def test_mark_as_read_requires_post_and_csrf(seeded, alice, make_message):
    from django.test import Client

    message = make_message(alice)
    strict = Client(enforce_csrf_checks=True)
    strict.force_login(alice)
    assert strict.get(f"{MESSAGES}{message.pk}/lu/").status_code == 405
    assert strict.post(f"{MESSAGES}{message.pk}/lu/").status_code == 403
    message.refresh_from_db()
    assert message.is_read is False


def test_messages_are_paginated(client, seeded, alice, make_message):
    for i in range(12):
        make_message(alice, subject=f"Message {i:02d}")
    client.force_login(alice)
    assert "Page 1 sur 2" in _html(client, MESSAGES)
    assert "Page 2 sur 2" in _html(client, MESSAGES + "?page=2")


def test_unread_badge_in_navigation(client, seeded, alice, make_message):
    make_message(alice)
    make_message(alice)
    client.force_login(alice)
    assert "Communications (2)" in _html(client, REQUESTS)


# ---- shell: a11y, i18n, RTL, headers ---------------------------------------------------------
@pytest.mark.parametrize("path", ALL_PAGES)
def test_every_page_has_landmarks_one_h1_breadcrumbs_and_private_headers(client, seeded, alice, path):
    client.force_login(alice)
    response = client.get(path)
    html = response.content.decode()
    assert response.status_code == 200
    assert len(re.findall(r"<h1[\s>]", html)) == 1
    assert '<main id="main-content"' in html and 'class="breadcrumbs' in html
    assert 'aria-current="page"' in html
    assert 'name="robots" content="noindex' in html
    cache_control = response["Cache-Control"]
    assert "no-store" in cache_control and "private" in cache_control
    assert not re.search(r'\sstyle="', html) and not re.search(r'\son[a-z]+="', html)
    externals = [u for u in re.findall(r'(?:src|href)="(https?://[^"]+)"', html) if "testserver" not in u]
    assert externals == []


@pytest.mark.parametrize("lang", ["fr", "it", "en", "ar"])
def test_four_languages_render_with_correct_direction(client, seeded, alice, lang, make_message, make_deadline):
    make_message(alice, subject="Objet")
    make_deadline(alice)
    client.force_login(alice)
    for path in ALL_PAGES:
        html = _html(client, path.replace("/fr/", f"/{lang}/", 1))
        assert f'<html lang="{lang}"' in html
        assert ('dir="rtl"' in html.split(">", 2)[1]) == (lang == "ar")
    dashboard = _html(client, DASHBOARD.replace("/fr/", f"/{lang}/", 1))
    if lang != "fr":
        assert '<span lang="fr">ESPACE RÉSERVÉ</span>' in dashboard, "French fallback is marked with lang"


def test_kill_switch_renders_503_for_accounts_but_not_for_staff(client, seeded, alice, staff_user):
    settings_row = SiteSettings.load()
    settings_row.reserved_area_enabled = False
    settings_row.save()
    client.force_login(alice)
    response = client.get(DASHBOARD)
    assert response.status_code == 503
    assert "portal-card" not in response.content.decode()
    client.force_login(staff_user)
    assert client.get(DASHBOARD).status_code == 200


def test_login_redirect_lands_on_the_dashboard(settings):
    from django.shortcuts import resolve_url
    from django.utils import translation

    with translation.override("fr"):
        assert resolve_url(settings.LOGIN_REDIRECT_URL) == DASHBOARD
