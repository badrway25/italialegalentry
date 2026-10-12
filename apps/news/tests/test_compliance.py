"""Compliance: locked texts rendered verbatim, no forbidden formulation, no external resource on news pages."""

import re

import pytest
from django.conf import settings

from cms import locked_content
from cms.forbidden import scan

pytestmark = [pytest.mark.compliance, pytest.mark.django_db]

LANGS = [code for code, _ in settings.LANGUAGES]


@pytest.fixture
def own_seeds(db):
    """Only this app's seeds plus the foundation ones (robust to sibling apps still under construction)."""
    from django.core.management import call_command

    for prefix in ("accounts.", "legal.", "consents.", "news."):
        call_command("seed_all", only=prefix, verbosity=0)


@pytest.fixture
def news_pages(client, own_seeds, phase3_open, newsletter_on, legal_published, article_factory):
    article_factory(
        "Article de conformité",
        slug="conformite",
        source_links=[{"label": "Source officielle", "url": "https://www.normattiva.it/"}],
    )
    pages = []
    for lang in LANGS:
        for path in ("actualites/", "actualites/?categorie=forum", "actualites/conformite/"):
            r = client.get(f"/{lang}/{path}")
            assert r.status_code == 200, (lang, path)
            pages.append((lang, path, r.content.decode()))
    return pages


def test_locked_news_texts_rendered_verbatim(news_pages):
    for lang, path, html in news_pages:
        if path.startswith("actualites/") and not path.startswith("actualites/conformite"):
            for key in ("p3.news.title", "p3.news.body", "p3.news.newsletter_label", "p3.news.newsletter_consent"):
                assert locked_content.text(key, "fr") in html, (lang, path, key)
            if lang != "fr":
                assert 'lang="fr"' in html, (lang, path)


def test_no_forbidden_formulations(news_pages):
    for lang, path, html in news_pages:
        assert not scan(html), (lang, path, scan(html))
        assert "®" not in html
        assert "Italy Legal Entry™" in html


def test_no_external_resources(news_pages):
    for lang, path, html in news_pages:
        srcs = re.findall(r'(?:src|href)="(https?://[^"]+)"', html)
        externals = [s for s in srcs if "testserver" not in s and "localhost" not in s]
        # The only external URL allowed is the plain <a rel="noopener noreferrer"> source link in the body.
        assert externals in ([], ["https://www.normattiva.it/"]), (lang, path, externals)
        assert "<iframe" not in html and '<script src="http' not in html
        emails = set(re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}", html))
        assert emails <= {"contact@agamieuromed.org"}, (lang, path, emails)


def test_no_placeholder_markers_public(news_pages):
    for lang, path, html in news_pages:
        for marker in ("CONTENT_PENDING_LEGAL_REVIEW", "lorem ipsum", "TODO"):
            assert marker not in html, (lang, path, marker)


def test_news_index_registered_as_public_route():
    from core.public_routes import all_routes

    assert any(r.app == "news" and r.path == "actualites/" and not r.requires_gate for r in all_routes())


def test_newsletter_consent_is_separate_purpose():
    from consents.models import ConsentPurpose
    from consents.services import LOCKED_CONSENT_KEYS

    assert LOCKED_CONSENT_KEYS[ConsentPurpose.NEWSLETTER] == "p3.news.newsletter_consent"
