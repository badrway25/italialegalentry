import pytest
from django.contrib.admin.sites import AdminSite
from django.contrib.messages.storage.fallback import FallbackStorage
from django.core.exceptions import PermissionDenied

from cms.models import PublicationStatus
from living.admin import LivingSheetAdmin, LivingTopicAdmin
from living.models import LegalReviewStatus, LivingSheet, LivingTopic

pytestmark = pytest.mark.django_db


def _request(rf, user):
    request = rf.post("/backoffice/living/livingsheet/")
    request.user = user
    request.session = {}
    request._messages = FallbackStorage(request)
    return request


def test_publish_action_hidden_without_permission(rf, staff_user, publisher_user):
    model_admin = LivingSheetAdmin(LivingSheet, AdminSite())
    assert "action_publish" not in model_admin.get_actions(_request(rf, staff_user))
    assert "action_mark_reviewed" in model_admin.get_actions(_request(rf, staff_user))
    assert "action_publish" in model_admin.get_actions(_request(rf, publisher_user))


def test_status_readonly_and_save_guard(rf, staff_user, publisher_user, sheet_factory):
    sheet = sheet_factory("G", slug="g", status=PublicationStatus.DRAFT)
    model_admin = LivingSheetAdmin(LivingSheet, AdminSite())
    assert "status" in model_admin.get_readonly_fields(_request(rf, staff_user), sheet)
    assert "status" not in model_admin.get_readonly_fields(_request(rf, publisher_user), sheet)
    sheet.status = PublicationStatus.PUBLISHED
    with pytest.raises(PermissionDenied):
        model_admin.save_model(_request(rf, staff_user), sheet, None, True)


def test_actions_enforce_review_and_permission(rf, staff_user, publisher_user, sheet_factory):
    sheet = sheet_factory("A", slug="a", status=PublicationStatus.DRAFT, reviewed=False)
    model_admin = LivingSheetAdmin(LivingSheet, AdminSite())
    qs = LivingSheet.objects.filter(pk=sheet.pk)
    staff_request = _request(rf, staff_user)
    model_admin.action_submit_for_review(staff_request, qs)
    sheet.refresh_from_db()
    assert sheet.status == PublicationStatus.REVIEW
    pub_request = _request(rf, publisher_user)
    model_admin.action_publish(pub_request, qs)
    sheet.refresh_from_db()
    assert sheet.status == PublicationStatus.REVIEW, "CONTENT_PENDING_LEGAL_REVIEW blocks publication"
    assert any("revue juridique" in str(m) for m in pub_request._messages)
    model_admin.action_mark_reviewed(staff_request, qs)
    sheet.refresh_from_db()
    assert sheet.legal_review == LegalReviewStatus.REVIEWED and sheet.reviewer == staff_user
    model_admin.action_publish(staff_request, qs)
    sheet.refresh_from_db()
    assert sheet.status == PublicationStatus.REVIEW, "staff without permission cannot publish"
    model_admin.action_publish(_request(rf, publisher_user), qs)
    sheet.refresh_from_db()
    assert sheet.status == PublicationStatus.PUBLISHED


def test_admin_pages_render(client, superuser, topics, sheet_factory):
    sheet = sheet_factory("Rendu", slug="rendu", sources=[{"label": "Src", "url": "https://example.org/"}])
    client.force_login(superuser)
    assert client.get("/backoffice/living/livingtopic/").status_code == 200
    topic = LivingTopic.objects.get(slug="logement")
    assert client.get(f"/backoffice/living/livingtopic/{topic.pk}/change/").status_code == 200
    assert client.get("/backoffice/living/livingsheet/").status_code == 200
    assert client.get(f"/backoffice/living/livingsheet/{sheet.pk}/change/").status_code == 200
    assert client.get("/backoffice/living/livingsheet/add/").status_code == 200


def test_topic_admin_columns(rf, topics, sheet_factory):
    sheet_factory("A", slug="a")
    sheet_factory("Draft", slug="d", status=PublicationStatus.DRAFT)
    model_admin = LivingTopicAdmin(LivingTopic, AdminSite())
    topic = LivingTopic.objects.get(slug="logement")
    assert model_admin.sheet_counts(topic) == "1 / 2"
    assert "IT: missing" in str(model_admin.translations(topic))
