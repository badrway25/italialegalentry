import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.exceptions import PermissionDenied

from cms.models import PublicationStatus
from news.admin import ArticleAdmin, NewsCategoryAdmin
from news.models import Article, NewsCategory

pytestmark = pytest.mark.django_db


def _request(rf, user):
    request = rf.post("/backoffice/news/article/")
    request.user = user
    request.session = {}
    request._messages = FallbackStorage(request)
    return request


def test_publish_action_hidden_from_staff_without_permission(rf, staff_user, publisher_user, superuser):
    site = AdminSite()
    model_admin = ArticleAdmin(Article, site)
    assert "action_publish" not in model_admin.get_actions(_request(rf, staff_user))
    assert "action_submit_for_review" in model_admin.get_actions(_request(rf, staff_user))
    assert "action_publish" in model_admin.get_actions(_request(rf, publisher_user))
    assert "action_publish" in model_admin.get_actions(_request(rf, superuser))


def test_status_readonly_for_staff_without_publish_permission(rf, staff_user, publisher_user, article_factory):
    article = article_factory("R", slug="r", status=PublicationStatus.DRAFT)
    model_admin = ArticleAdmin(Article, AdminSite())
    ro_staff = model_admin.get_readonly_fields(_request(rf, staff_user), article)
    assert {"status", "publish_at", "unpublish_at", "editor", "published_at", "version"} <= set(ro_staff)
    ro_pub = model_admin.get_readonly_fields(_request(rf, publisher_user), article)
    assert "status" not in ro_pub


def test_save_model_blocks_publication_without_permission(rf, staff_user, publisher_user, article_factory):
    article = article_factory("S", slug="s", status=PublicationStatus.DRAFT)
    model_admin = ArticleAdmin(Article, AdminSite())
    article.status = PublicationStatus.PUBLISHED
    with pytest.raises(PermissionDenied):
        model_admin.save_model(_request(rf, staff_user), article, None, True)
    article.refresh_from_db()
    assert article.status == PublicationStatus.DRAFT
    article.status = PublicationStatus.PUBLISHED
    model_admin.save_model(_request(rf, publisher_user), article, None, True)
    article.refresh_from_db()
    assert article.status == PublicationStatus.PUBLISHED
    assert article.editor == publisher_user


def test_actions_run_workflow_with_messages(rf, staff_user, publisher_user, article_factory):
    article = article_factory("A", slug="a", status=PublicationStatus.DRAFT)
    model_admin = ArticleAdmin(Article, AdminSite())
    request = _request(rf, staff_user)
    model_admin.action_submit_for_review(request, Article.objects.filter(pk=article.pk))
    article.refresh_from_db()
    assert article.status == PublicationStatus.REVIEW
    # staff without permission calling the action directly is still refused by the service
    model_admin.action_publish(request, Article.objects.filter(pk=article.pk))
    article.refresh_from_db()
    assert article.status == PublicationStatus.REVIEW
    assert any("Permission refusée" in str(m) for m in request._messages)
    request = _request(rf, publisher_user)
    model_admin.action_publish(request, Article.objects.filter(pk=article.pk))
    article.refresh_from_db()
    assert article.status == PublicationStatus.PUBLISHED
    model_admin.action_archive(request, Article.objects.filter(pk=article.pk))
    article.refresh_from_db()
    assert article.status == PublicationStatus.ARCHIVED


def test_admin_changelist_and_change_form_render(client, superuser, article_factory, categories):
    article = article_factory(
        "Rendu admin", slug="rendu", source_links=[{"label": "Src", "url": "https://example.org/"}]
    )
    client.force_login(superuser)
    assert client.get("/backoffice/news/article/").status_code == 200
    r = client.get(f"/backoffice/news/article/{article.pk}/change/")
    assert r.status_code == 200
    assert client.get("/backoffice/news/newscategory/").status_code == 200
    assert client.get("/backoffice/news/article/add/").status_code == 200


def test_category_admin_columns(rf, superuser, categories, article_factory):
    article_factory("X", slug="x")
    model_admin = NewsCategoryAdmin(NewsCategory, AdminSite())
    cat = NewsCategory.objects.get(slug="normativa")
    assert model_admin.article_count(cat) == 1


def test_translation_matrix_column(article_factory):
    from news.admin import translation_matrix_html

    article = article_factory("T", slug="t")
    html = str(translation_matrix_html(article))
    assert "IT: missing" in html and "EN: missing" in html and "AR: missing" in html
    assert "FR" not in html
