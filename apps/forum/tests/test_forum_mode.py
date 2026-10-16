"""Gate G4 — switch to « FORUM PERMANENT VÉNÉTIE–MAROC » by flag/date or override; permanent sections."""

from __future__ import annotations

import datetime as dt

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from freezegun import freeze_time

from cms import locked_content
from cms.forbidden import scan
from cms.models import PublicationStatus
from core import flags
from forum.models import ForumAgreement, ForumDocument, ForumIntervention, ForumNextEvent, ForumOutcome
from forum.tests.conftest import EVENT_END_ROME, ROME

pytestmark = pytest.mark.django_db

PERMANENT_TITLE = "FORUM PERMANENT VÉNÉTIE–MAROC"
PDF = b"%PDF-1.4\n%test\n1 0 obj<<>>endobj\ntrailer<<>>\n%%EOF\n"


def _page(client, lang="fr"):
    response = client.get(f"/{lang}/forum/")
    assert response.status_code == 200
    return response.content.decode()


def test_switch_to_permanent_by_flag_with_frozen_time(client, event, set_flag):
    set_flag("forum_permanent_mode", True, enabled_from=EVENT_END_ROME)
    with freeze_time(dt.datetime(2026, 10, 2, 17, 30, tzinfo=ROME)):
        flags.invalidate()
        html = _page(client)
        assert PERMANENT_TITLE not in html
        assert 'id="forum-registration"' in html
        assert 'type="application/ld+json"' in html
    with freeze_time(dt.datetime(2026, 10, 2, 18, 30, tzinfo=ROME)):
        flags.invalidate()
        html = _page(client)
        assert f'forum-hero__title">{PERMANENT_TITLE}</h1>' in html
        assert 'id="forum-registration"' not in html
        assert 'type="application/ld+json"' not in html
        assert "page-forum--permanent" in html


def test_flag_without_date_does_not_switch_before_event_end(client, event, set_flag):
    set_flag("forum_permanent_mode", False, enabled_from=EVENT_END_ROME)
    with freeze_time(dt.datetime(2026, 10, 5, 12, 0, tzinfo=ROME)):
        flags.invalidate()
        assert PERMANENT_TITLE not in _page(client), "date alone must not switch without the flag"


def test_manual_override_switches_immediately(client, permanent_event):
    html = _page(client)
    assert PERMANENT_TITLE in html
    assert "PARTICIPEZ AU FORUM" not in html
    # the presentation sections and the programme stay (no structural rewrite)
    for key in ("who.title", "why.title", "what.title", "objectives.title", "audience.title", "programme.title"):
        assert locked_content.text(f"p2.forum.{key}", "fr") in html


def test_registration_closed_in_permanent_mode(client, permanent_event, forms_open):
    html = _page(client)
    assert 'id="forum-registration-form"' not in html
    response = client.get("/fr/forum/inscription/")
    assert response.status_code == 200
    assert 'data-registration="closed"' in response.content.decode()
    response = client.post("/fr/forum/inscription/", {"first_name": "x"})
    assert response.status_code == 403


def test_permanent_sections_render_only_published_rows(client, permanent_event, published):
    event = permanent_event
    html = _page(client)
    for anchor in ("forum-outcomes", "forum-documents", "forum-interventions", "forum-agreements", "forum-next-events"):
        assert f'id="{anchor}"' not in html, "empty sections are hidden"
    ForumOutcome.objects.create(event=event, title="Résultat brouillon", text="Texte", status=PublicationStatus.DRAFT)
    assert "Résultat brouillon" not in _page(client)
    published(ForumOutcome.objects.create(event=event, title="Résultat publié", text="Texte du résultat"))
    doc = published(
        ForumDocument.objects.create(
            event=event, title="Document public", file=SimpleUploadedFile("doc-test.pdf", PDF, "application/pdf")
        )
    )
    published(
        ForumIntervention.objects.create(
            event=event, title="Intervention publiée", speaker=event.speaker_roles.first(), document=doc
        )
    )
    published(
        ForumAgreement.objects.create(
            event=event, title="Convention publiée", parties="AGAMI — Partenaire", kind="convention"
        )
    )
    published(
        ForumNextEvent.objects.create(
            event=event,
            title="Rencontre à Casablanca",
            date=dt.date(2026, 10, 29),
            place="Casablanca",
            url="https://example.org/agenda",
        )
    )
    published(
        ForumNextEvent.objects.create(
            event=event, title="Rencontre interne", date=dt.date(2026, 10, 30), url="/fr/forum/"
        )
    )
    html = _page(client)
    for anchor in ("forum-outcomes", "forum-documents", "forum-interventions", "forum-agreements", "forum-next-events"):
        assert f'id="{anchor}"' in html, anchor
    assert "Résultat publié" in html and "Résultat brouillon" not in html
    assert "Document public (PDF)" in html and 'type="application/pdf"' in html
    assert "Intervention publiée" in html and "Sénateur de la République" in html
    assert "Convention publiée" in html
    assert "Rencontre à Casablanca" in html
    assert 'href="https://example.org/agenda"' not in html, "external links are never rendered as hrefs"
    assert 'href="/fr/forum/">Rencontre interne' in html
    assert not scan(html)


def test_scheduled_rows_follow_clock(client, permanent_event):
    row = ForumOutcome.objects.create(
        event=permanent_event,
        title="Résultat programmé",
        text="Texte",
        status=PublicationStatus.SCHEDULED,
        publish_at=dt.datetime(2026, 11, 1, 9, 0, tzinfo=ROME),
    )
    with freeze_time(dt.datetime(2026, 10, 31, 12, 0, tzinfo=ROME)):
        assert row.title not in _page(client)
    with freeze_time(dt.datetime(2026, 11, 1, 12, 0, tzinfo=ROME)):
        assert row.title in _page(client)


def test_virtual_forum_teaser_gated(client, permanent_event, set_flag):
    html = _page(client)
    assert 'data-gate="virtual-forum"' not in html
    assert locked_content.text("p3.virtual_forum.title", "fr") not in html
    set_flag("virtual_forum", True)
    html = _page(client)
    assert 'data-gate="virtual-forum"' in html
    assert locked_content.text("p3.virtual_forum.title", "fr") in html
    assert locked_content.text("p3.virtual_forum.button", "fr") in html


def test_virtual_forum_teaser_not_in_event_mode(client, event, set_flag):
    set_flag("virtual_forum", True)
    assert 'data-gate="virtual-forum"' not in _page(client)


def test_permanent_mode_compliance_all_languages(client, permanent_event, set_flag):
    set_flag("virtual_forum", True)
    for lang in ("fr", "it", "en", "ar"):
        html = _page(client, lang)
        assert not scan(html), lang
        assert "Italy Legal Entry™" in html
