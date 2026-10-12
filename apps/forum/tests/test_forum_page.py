"""Integration tests — public Forum page (event mode), gates G5/G6, SEO, RTL, sitemap."""

from __future__ import annotations

import re

import pytest
from django.utils.html import escape

from cms import locked_content
from cms.forbidden import scan
from cms.models import MediaAsset
from forum.models import PartnerKind

pytestmark = pytest.mark.django_db

SECTION_KEYS = (
    ("forum-who", "p2.forum.who.title"),
    ("forum-why", "p2.forum.why.title"),
    ("forum-what", "p2.forum.what.title"),
    ("forum-objectives", "p2.forum.objectives.title"),
    ("forum-audience", "p2.forum.audience.title"),
    ("forum-programme", "p2.forum.programme.title"),
    ("forum-speakers", "p2.forum.speakers.title"),
    ("forum-registration", "p2.forum.registration.title"),
    ("forum-cta", None),
)


def _text(key: str) -> str:
    return escape(locked_content.text(key, "fr"))


def _page(client, lang="fr"):
    response = client.get(f"/{lang}/forum/")
    assert response.status_code == 200
    return response.content.decode()


@pytest.mark.parametrize("lang", ["fr", "it", "en", "ar"])
def test_page_200_all_languages(client, event, lang):
    html = _page(client, lang)
    assert _text("p2.forum.header.title") in html
    if lang != "fr":
        assert 'lang="fr"' in html, "fallback texts must carry lang=fr"


def test_header_texts(client, event):
    html = _page(client)
    for key in ("header.title", "header.subtitle", "header.meta", "header.patronage"):
        assert _text(f"p2.forum.{key}") in html
    assert html.count("<h1") == 1
    assert 'datetime="2026-10-02T15:00:00+02:00"' in html


def test_sections_present_in_prescribed_order(client, event):
    html = _page(client)
    body = html[html.index('class="forum-sections"') :]
    positions = []
    for anchor, key in SECTION_KEYS:
        idx = body.index(f'id="{anchor}"')
        positions.append(idx)
        if key:
            assert _text(key) in body[idx:], key
    assert positions == sorted(positions)


def test_who_why_objectives_audience_bodies(client, event):
    html = _page(client)
    for key in ("who.body", "why.body", "objectives.body", "audience.body", "programme.note", "speakers.body"):
        assert _text(f"p2.forum.{key}") in html, key


def test_what_three_paragraphs(client, event):
    html = _page(client)
    paragraphs = locked_content.get("p2.forum.what.body", "fr")[0]
    assert len(paragraphs) == 3
    for p in paragraphs:
        assert f"<p>{escape(p)}</p>" in html


def test_programme_seed_order_and_note(client, event):
    html = _page(client)
    start = html.index('id="forum-programme"')
    section = html[start : html.index('id="forum-speakers"')]
    titles = re.findall(r'forum-programme__title">([^<]+)<', section)
    assert titles[0] == "Accueil et enregistrement"
    assert titles[-1] == "Conclusions et prochaines étapes"
    assert len(titles) == 8
    assert 'forum-programme__time">15h00<' in section
    assert _text("p2.forum.programme.note") in section


def test_programme_is_editable_and_reflected(client, event):
    item = event.programme_items.order_by("order").first()
    item.title_fr = "Accueil des participants (modifié)"
    item.time_label = "14h30"
    item.save()
    html = _page(client)
    assert "Accueil des participants (modifié)" in html
    assert "14h30" in html


def test_speakers_functions_only(client, event):
    html = _page(client)
    section = html[html.index('id="forum-speakers"') : html.index('id="forum-registration"')]
    for role in locked_content.get("p2.forum.speakers.roles", "fr")[0]:
        assert escape(role) in section
    assert "forum-speakers__name" not in section


def test_no_person_names_public_without_both_authorisations(client, event, speaker_names_flag):
    role = event.speaker_roles.first()
    role.person_name = "Mario Rossi Test"
    role.organisation = "Organisation Test"
    role.save()
    # 1) neither authorised
    assert "Mario Rossi Test" not in _page(client)
    # 2) record authorised, flag off
    role.names_authorized = True
    role.authorization_reference = "e-mail de l’Avv. Badrane du 2026-09-30"
    role.save()
    html = _page(client)
    assert "Mario Rossi Test" not in html and "Organisation Test" not in html
    # 3) flag on, record NOT authorised
    role.names_authorized = False
    role.save()
    speaker_names_flag(True)
    assert "Mario Rossi Test" not in _page(client)
    # 4) both → name rendered
    role.names_authorized = True
    role.authorization_reference = "e-mail de l’Avv. Badrane du 2026-09-30"
    role.save()
    html = _page(client)
    assert "Mario Rossi Test" in html and "Organisation Test" in html


def test_patronage_no_fake_logos(client, event):
    html = _page(client)
    hero = html[html.index('class="forum-hero') : html.index('class="forum-localnav')]
    assert _text("p2.forum.header.patronage") in hero
    assert "<img" not in hero, "unauthorised partners must never render a logo"
    assert "Regione del Veneto" not in html and "Comune di Rovigo" not in html
    assert "forum-hero__logos" not in html


def test_authorised_partner_with_logo_renders(client, event, tmp_path, settings):
    from django.core.files.uploadedfile import SimpleUploadedFile

    png = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
        b"\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    asset = MediaAsset.objects.create(
        title="Logo test",
        file=SimpleUploadedFile("logo-test.png", png, "image/png"),
        alt_fr="Logo test",
        license="client",
    )
    partner = event.partners.get(name="Regione del Veneto")
    partner.logo = asset
    partner.kind = PartnerKind.PATRON
    partner.save()
    assert "forum-hero__logos" not in _page(client), "logo without authorisation stays hidden"
    partner.authorized = True
    partner.authorization_reference = "autorizzazione scritta del 2026-10-01"
    partner.save()
    html = _page(client)
    assert "forum-hero__logos" in html and 'alt="Regione del Veneto"' in html


# The registration form exists only until the event ends (2 Oct 2026, 18:00 Rome): the three tests
# about it run at a moment before the Forum (``before_the_forum``), never on the real date.
def test_registration_section_and_ctas(before_the_forum, client, event):
    html = _page(client)
    assert _text("p2.forum.registration.title") in html
    assert _text("p2.forum.registration.intro") in html
    assert _text("p2.forum.registration.button_primary") in html
    assert _text("p2.forum.registration.button_secondary_pilot") in html
    assert _text("p2.forum.registration.button_secondary_collab") in html
    assert 'href="#forum-registration"' in html
    assert 'href="/it/privacy-policy/"' in html


def test_form_unavailable_while_forms_gate_closed(before_the_forum, client, event):
    html = _page(client)
    assert 'data-gate="forms-closed"' in html
    assert 'id="forum-registration-form"' not in html


def test_form_rendered_when_forms_gate_open(before_the_forum, client, event, forms_open):
    html = _page(client)
    assert 'id="forum-registration-form"' in html
    assert 'data-gate="forms-closed"' not in html


def test_jsonld_only_in_event_mode(client, event):
    html = _page(client)
    assert 'type="application/ld+json"' in html
    assert '"@type": "Event"' in html
    event.mode_override = "permanent"
    event.save()
    html = _page(client)
    assert 'type="application/ld+json"' not in html


def test_rtl_arabic_render(client_ar, event):
    response = client_ar.get("/ar/forum/")
    assert response.status_code == 200
    html = response.content.decode()
    assert '<html lang="ar" dir="rtl"' in html
    assert _text("p2.forum.header.title") in html


def test_sitemap_lists_forum_page(client, event):
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    xml = response.content.decode()
    assert "/fr/forum/" in xml and "/ar/forum/" in xml


def test_forum_routes_registered_as_public(event):
    from core.public_routes import ungated_paths

    assert {"forum/", "forum/inscription/", "forum/inscription/confirmation/"} <= set(ungated_paths())


def test_no_forbidden_strings_or_external_resources(client, event):
    for lang in ("fr", "it", "en", "ar"):
        html = _page(client, lang)
        assert not scan(html), lang
        assert "Italy Legal Entry™" in html
        externals = [s for s in re.findall(r'(?:src|href)="(https?://[^"]+)"', html) if "testserver" not in s]
        assert not externals, externals


def test_page_without_event_renders_empty_state(client, db):
    response = client.get("/fr/forum/")
    assert response.status_code == 200
    html = response.content.decode()
    assert _text("p2.forum.header.title") in html
    assert 'class="empty-state"' in html


def test_accessibility_landmarks(client, event):
    html = _page(client)
    assert html.count("<h1") == 1
    assert '<main id="main-content"' in html
    assert 'aria-label="Sections de la page"' in html
    assert 'aria-labelledby="forum-programme-title"' in html
