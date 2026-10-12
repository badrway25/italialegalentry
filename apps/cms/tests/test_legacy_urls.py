"""Legacy WordPress URL handling (docs/URL_MIGRATION_MAP.md) — redirects, 410 Gone, no open redirect."""

import pytest

from cms.models import Redirect

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize("lang", ["it", "fr", "en", "ar"])
def test_old_language_query_redirects_to_language_prefix(client, lang):
    response = client.get(f"/?lang={lang}")
    assert response.status_code == 301
    assert response["Location"] == f"/{lang}/"


def test_unknown_language_query_falls_back_to_root_redirect(client):
    response = client.get("/?lang=zz")
    assert response.status_code == 302  # core.views.root_redirect (Accept-Language negotiation)


@pytest.mark.parametrize("path", ["/wp-sitemap.xml", "/wp-sitemap-posts-page-1.xml"])
def test_wordpress_sitemaps_redirect_to_django_sitemap(client, path):
    response = client.get(path)
    assert response.status_code == 301
    assert response["Location"] == "/sitemap.xml"


@pytest.mark.parametrize(
    "path",
    [
        "/wp-json/",
        "/wp-json/wp/v2/users",
        "/wp-login.php",
        "/wp-admin/",
        "/xmlrpc.php",
        "/readme.html",
        "/hello-world/",
        "/category/uncategorized/",
        "/author/someone/",
        "/feed/",
        "/comments/feed/",
        "/wp-content/themes/italy-template/style.css",
    ],
)
def test_wordpress_endpoints_are_gone(client, path):
    response = client.get(path)
    assert response.status_code == 410
    html = response.content.decode()
    assert "Italy Legal Entry™" in html
    assert "410" in html


def test_gone_page_is_a_full_institutional_page(client):
    html = client.get("/hello-world/").content.decode()
    assert html.count("<h1") == 1
    assert 'id="main-content"' in html


def test_redirect_rows_apply_only_to_missing_pages(client):
    Redirect.objects.create(old_path="/vecchia-pagina/", new_path="/fr/forum/", permanent=True)
    Redirect.objects.create(old_path="/fr/privacy-policy/", new_path="/fr/", permanent=True)
    response = client.get("/vecchia-pagina/")
    assert response.status_code == 301 and response["Location"] == "/fr/forum/"
    assert client.get("/vecchia-pagina").status_code == 301, "trailing slash variants match"
    assert client.get("/fr/privacy-policy/").status_code == 200, "a real page is never shadowed"


def test_temporary_redirect_row(client):
    Redirect.objects.create(old_path="/temp/", new_path="/fr/", permanent=False)
    assert client.get("/temp/").status_code == 302


@pytest.mark.security
@pytest.mark.parametrize("target", ["https://evil.example/", "//evil.example/", "javascript:alert(1)"])
def test_redirect_table_cannot_become_an_open_redirect(client, target):
    Redirect.objects.create(old_path="/uscita/", new_path=target)
    assert client.get("/uscita/").status_code == 404


def test_unknown_path_is_still_404(client):
    assert client.get("/fr/pagina-che-non-esiste/").status_code == 404
