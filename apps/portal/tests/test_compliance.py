"""Compliance: prescribed texts only through the locked registry, no forbidden formulation, clean assets."""

from __future__ import annotations

import re
from pathlib import Path

import pytest
from django.conf import settings
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.utils import translation
from django.utils.html import escape

from cms import locked_content
from cms.forbidden import scan
from portal.tests.conftest import DASHBOARD, DEADLINES, DOCUMENTS, MESSAGES, PATHWAYS, REQUESTS

pytestmark = pytest.mark.compliance

BASE_DIR = Path(settings.BASE_DIR)
TEMPLATES = BASE_DIR / "templates" / "portal"
PORTAL_APP = BASE_DIR / "apps" / "portal"
RESERVED_KEYS = ("p3.reserved.title", "p3.reserved.body", "p3.reserved.button")


def _template_files() -> list[Path]:
    return sorted(TEMPLATES.rglob("*.html"))


@pytest.mark.django_db
def test_landing_renders_the_prescribed_title_and_body(client, seeded, alice):
    client.force_login(alice)
    html = client.get(DASHBOARD).content.decode()
    title = locked_content.text("p3.reserved.title", "fr")
    body = locked_content.text("p3.reserved.body", "fr")
    assert re.search(rf"<h1[^>]*>\s*{re.escape(escape(title))}\s*</h1>", html), "locked title is the single h1"
    assert escape(body) in html


@pytest.mark.django_db
def test_access_point_partial_renders_title_body_and_button_for_anonymous_visitors(seeded):
    """The prescribed access point (title + sentence + CONNEXION button) offered to the public pages."""
    from django.contrib.auth.models import AnonymousUser

    request = RequestFactory().get("/fr/")
    request.user = AnonymousUser()
    with translation.override("fr"):
        html = render_to_string("portal/partials/access_point.html", {"user": request.user}, request=request)
    for key in RESERVED_KEYS:
        assert escape(locked_content.text(key, "fr")) in html, key
    assert 'href="/fr/compte/login/?next=/fr/espace-reserve/"' in html
    with translation.override("ar"):
        html_ar = render_to_string("portal/partials/access_point.html", {"user": request.user}, request=request)
    assert html_ar.count('lang="fr"') == 3, "official French wording, marked as such, until a translation is approved"


@pytest.mark.django_db
def test_access_point_partial_offers_the_dashboard_to_a_signed_in_account(seeded, alice):
    request = RequestFactory().get("/fr/")
    request.user = alice
    with translation.override("fr"):
        html = render_to_string("portal/partials/access_point.html", {"user": alice}, request=request)
    assert 'href="/fr/espace-reserve/"' in html
    assert escape(locked_content.text("p3.reserved.button", "fr")) not in html


def test_prescribed_texts_are_never_hand_copied():
    """Templates and code reach the prescribed wording only through {% locked %} / locked_content."""
    samples = [locked_content.text(key, "fr") for key in RESERVED_KEYS[:2]]
    samples.append(locked_content.text("p3.persons.how_it_works", "fr"))
    files = _template_files() + sorted(PORTAL_APP.glob("*.py"))
    assert len(_template_files()) >= 9
    for path in files:
        text = path.read_text(encoding="utf-8")
        for sample in samples:
            assert sample not in text, (path.name, sample)
    dashboard = (TEMPLATES / "dashboard.html").read_text(encoding="utf-8")
    assert '{% locked "p3.reserved.title"' in dashboard and '{% locked "p3.reserved.body"' in dashboard
    access = (TEMPLATES / "partials" / "access_point.html").read_text(encoding="utf-8")
    for key in RESERVED_KEYS:
        assert f'{{% locked "{key}" %}}' in access


def test_templates_have_no_forbidden_strings_inline_styles_handlers_or_external_urls():
    for path in _template_files():
        text = path.read_text(encoding="utf-8")
        assert scan(text) == [], (path.name, scan(text))
        assert not re.search(r"\sstyle=\"", text), path.name
        assert not re.search(r"\son[a-z]+=\"", text), path.name
        assert not re.search(r"https?://", text), path.name
        assert "®" not in text and "legalitalentry.it" not in text, path.name


def test_every_icon_used_exists_in_the_sprite():
    sprite = (BASE_DIR / "static" / "img" / "icons.svg").read_text(encoding="utf-8")
    ids = set(re.findall(r'<symbol id="icon-([a-z0-9-]+)"', sprite))
    used = set()
    for path in _template_files():
        used |= set(re.findall(r'svg_icon "([a-z0-9-]+)"', path.read_text(encoding="utf-8")))
    used |= set(re.findall(r'icon="([a-z0-9-]+)"', (PORTAL_APP / "services.py").read_text(encoding="utf-8")))
    assert used and not (used - ids), used - ids


def test_stylesheet_uses_tokens_and_logical_properties_only():
    css = (PORTAL_APP / "static" / "portal" / "portal.css").read_text(encoding="utf-8")
    assert re.findall(r"#[0-9a-fA-F]{3,8}\b", css) == [], "no literal colours — design tokens only"
    assert not re.search(r"\brgba?\(|\bhsla?\(", css)
    assert not re.search(r"https?://", css)
    physical = re.findall(
        r"(?<![-\w])(?:margin|padding|border)-(?:left|right)\b|(?<![-\w])(?:left|right)\s*:|text-align:\s*(?:left|right)",
        css,
    )
    assert physical == [], physical


def test_ui_strings_are_wrapped_for_translation():
    """French source strings in templates go through {% translate %} / {% blocktranslate %}."""
    for path in _template_files():
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"{% comment %}.*?{% endcomment %}", "", text, flags=re.S)
        text = re.sub(r"{% blocktranslate.*?{% endblocktranslate %}", "", text, flags=re.S)
        text = re.sub(r"{% block body_class %}.*?{% endblock %}", "", text, flags=re.S)  # CSS class, not UI text
        text = re.sub(r"{%.*?%}|{{.*?}}", "", text, flags=re.S)
        text = re.sub(r"<[^>]+>", " ", text)
        leftovers = re.findall(r"[A-Za-zÀ-ÿ’']{4,}", text)
        assert leftovers == [], (path.name, leftovers[:5])


@pytest.mark.django_db
def test_rendered_pages_are_free_of_forbidden_formulations(
    client, seeded, alice, make_contact_request, make_message, make_deadline, make_document, completed_orientation
):
    make_contact_request(alice)
    message = make_message(alice)
    make_deadline(alice)
    make_document(alice)
    completed_orientation(alice)
    client.force_login(alice)
    for lang in ("fr", "it", "en", "ar"):
        for path in (DASHBOARD, REQUESTS, PATHWAYS, DOCUMENTS, DEADLINES, MESSAGES, f"{MESSAGES}{message.pk}/"):
            response = client.get(path.replace("/fr/", f"/{lang}/", 1))
            assert response.status_code == 200, (lang, path)
            html = response.content.decode()
            assert scan(html) == [], (lang, path, scan(html))
            assert "Italy Legal Entry™" in html
            emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", html))
            assert emails <= {"contact@agamieuromed.org", alice.email}, (lang, path, emails)


def test_no_portal_route_is_registered_as_public():
    from core.public_routes import all_routes

    assert [r for r in all_routes() if r.app == "portal" or r.path.startswith("espace-reserve")] == []


def test_migrations_are_in_sync(db):
    from io import StringIO

    from django.core.management import call_command

    out = StringIO()
    call_command("makemigrations", "portal", "--check", "--dry-run", stdout=out, stderr=out)
