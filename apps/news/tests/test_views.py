import datetime as dt

import pytest
from django.contrib.sitemaps.views import sitemap
from django.test import Client
from freezegun import freeze_time

from cms.models import PublicationStatus, TranslationStatus
from news.models import ArticleTranslation
from news.sitemaps import ArticleSitemap, NewsIndexSitemap

pytestmark = pytest.mark.django_db

INDEX = "/fr/actualites/"


def test_index_renders_neutral_heading_before_phase3(client, categories, before_phase3):
    r = client.get(INDEX)
    assert r.status_code == 200
    html = r.content.decode()
    assert "<h1" in html and html.count("<h1") == 1
    assert "Actualités" in html
    assert "ACTUALITÉS" not in html, "locked Phase 3 header must not appear before the gate"
    assert "Nouveautés normatives" not in html
    assert "Aucune actualité publiée" in html


def test_index_renders_locked_texts_when_phase3_open(client, categories, phase3_open):
    html = client.get(INDEX).content.decode()
    assert "ACTUALITÉS" in html
    assert "Nouveautés normatives, échéances officielles, initiatives du Forum Permanent Vénétie–Maroc" in html
    assert html.count("<h1") == 1


def test_index_lists_only_live_articles_with_category_filter(client, article_factory, categories):
    from news.models import NewsCategory

    forum = NewsCategory.objects.get(slug="forum")
    article_factory("Visible", slug="visible")
    article_factory("Caché", slug="hidden", status=PublicationStatus.DRAFT)
    article_factory("Forum article", slug="forum-a", category=forum)
    html = client.get(INDEX).content.decode()
    assert "Visible" in html and "Forum article" in html and "Caché" not in html
    html = client.get(INDEX + "?categorie=forum").content.decode()
    assert "Forum article" in html and "Visible" not in html
    assert 'aria-current="true"' in html
    html = client.get(INDEX + "?categorie=unknown").content.decode()
    assert "Visible" in html, "unknown category is ignored"
    html = client.get(INDEX + "?categorie=echeances").content.decode()
    assert "Aucun article dans cette catégorie" in html


def test_index_pagination(client, article_factory):
    for i in range(12):
        article_factory(f"Article numéro {i}", slug=f"n-{i}")
    r = client.get(INDEX)
    html = r.content.decode()
    assert "Page 1 sur 2" in html
    assert 'rel="next"' in html
    html2 = client.get(INDEX + "?page=2").content.decode()
    assert "Page 2 sur 2" in html2
    assert 'rel="prev"' in html2
    assert client.get(INDEX + "?page=99").status_code == 200


def test_detail_404_for_draft_and_unknown(client, article_factory):
    article_factory("Brouillon", slug="draft", status=PublicationStatus.DRAFT)
    assert client.get("/fr/actualites/draft/").status_code == 404
    assert client.get("/fr/actualites/unknown/").status_code == 404


def test_detail_404_before_schedule(client, article_factory):
    with freeze_time("2026-10-05 10:00:00"):
        article_factory(
            "Futur",
            slug="future",
            status=PublicationStatus.SCHEDULED,
            publish_at=dt.datetime(2026, 10, 7, tzinfo=dt.UTC),
        )
        assert client.get("/fr/actualites/future/").status_code == 404
    with freeze_time("2026-10-08 10:00:00"):
        assert client.get("/fr/actualites/future/").status_code == 200


def test_detail_renders_article_metadata_body_sources_related_and_jsonld(client, article_factory, categories):
    related = article_factory("Article lié", slug="lie")
    article = article_factory(
        "Titre principal",
        slug="principal",
        published_at=dt.datetime(2026, 10, 3, 9, 0, tzinfo=dt.UTC),
        last_updated=dt.datetime(2026, 10, 6, 9, 0, tzinfo=dt.UTC),
        image_caption="Légende",
        source_links=[{"label": "Normattiva", "url": "https://www.normattiva.it/"}],
        seo_title="SEO titre",
        seo_description="SEO description",
    )
    article.related.add(related)
    r = client.get("/fr/actualites/principal/")
    assert r.status_code == 200
    html = r.content.decode()
    assert html.count("<h1") == 1 and "Titre principal" in html
    assert "Normativa" in html  # category
    assert "03.10.2026" in html and "06.10.2026" in html
    assert "<h2>Intertitre</h2>" in html
    assert "<li>point un</li>" in html
    assert 'href="https://www.normattiva.it/" rel="noopener noreferrer external"' in html
    assert "Article lié" in html
    assert '<script type="application/ld+json">' in html
    assert '"@type": "Article"' in html and '"datePublished"' in html
    assert '<meta property="og:type" content="article">' in html
    assert '<meta property="og:title" content="SEO titre">' in html
    assert '<meta name="twitter:card" content="summary">' in html
    assert '<link rel="canonical" href="http://testserver/fr/actualites/principal/">' in html
    assert 'hreflang="ar"' in html
    assert "<title>SEO titre · Italy Legal Entry™</title>" in html
    assert 'aria-current="page"' in html  # breadcrumbs
    assert "Fil d’Ariane" in html


def test_detail_uses_published_translation_only(client, article_factory):
    article = article_factory("Titre FR", slug="tr")
    ArticleTranslation.objects.create(
        master=article, language="en", title="English title", status=TranslationStatus.DRAFT
    )
    html = client.get("/en/actualites/tr/").content.decode()
    assert "Titre FR" in html and "English title" not in html
    assert 'lang="fr"' in html, "fallback text must be marked lang=fr"
    ArticleTranslation.objects.filter(master=article).update(status=TranslationStatus.PUBLISHED)
    html = client.get("/en/actualites/tr/").content.decode()
    assert "English title" in html


def test_staff_preview_of_unpublished_article(client, article_factory, staff_user, person_user):
    from accounts.roles import ensure_roles

    ensure_roles()  # role:staff gets news.view_article
    article_factory("Brouillon", slug="draft", status=PublicationStatus.DRAFT)
    client.force_login(person_user)
    assert client.get("/fr/actualites/draft/").status_code == 404
    client.force_login(staff_user)
    r = client.get("/fr/actualites/draft/")
    assert r.status_code == 200
    html = r.content.decode()
    assert 'name="robots" content="noindex' in html
    assert "Aperçu réservé à la rédaction" in html


def test_rtl_arabic_pages(client_ar, article_factory):
    article_factory("Article RTL", slug="rtl")
    r = client_ar.get("/ar/actualites/")
    assert r.status_code == 200
    assert '<html lang="ar" dir="rtl"' in r.content.decode()
    r = client_ar.get("/ar/actualites/rtl/")
    assert r.status_code == 200
    assert 'lang="fr"' in r.content.decode()


def test_only_get_on_index_and_detail(client, article_factory):
    article_factory("A", slug="a")
    assert client.post(INDEX).status_code == 405
    assert client.post("/fr/actualites/a/").status_code == 405


def test_sitemaps_list_only_live_articles(rf, article_factory):
    live = article_factory("Live", slug="live")
    article_factory("Draft", slug="draft", status=PublicationStatus.DRAFT)
    assert list(ArticleSitemap().items()) == [live]
    request = rf.get("/sitemap.xml")
    response = sitemap(request, sitemaps={"news": ArticleSitemap, "news_index": NewsIndexSitemap})
    response.render()
    xml = response.content.decode()
    assert "/fr/actualites/live/" in xml and "/ar/actualites/live/" in xml
    assert "/fr/actualites/draft/" not in xml
    assert "/fr/actualites/</loc>" in xml


def test_index_available_in_every_language(article_factory):
    article_factory("Multi", slug="multi")
    for lang in ("it", "fr", "en", "ar"):
        assert Client().get(f"/{lang}/actualites/").status_code == 200
        assert Client().get(f"/{lang}/actualites/multi/").status_code == 200
