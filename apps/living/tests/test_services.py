import pytest
from django.core.exceptions import PermissionDenied

from audit.models import AuditEvent
from cms.models import PublicationStatus
from living import services
from living.models import LegalReviewStatus, LivingTopic

pytestmark = pytest.mark.django_db


def test_public_topics_with_live_sheet_counts(topics, sheet_factory):
    sheet_factory("A", slug="a")
    sheet_factory("B", slug="b")
    sheet_factory("Draft", slug="d", status=PublicationStatus.DRAFT)
    LivingTopic.objects.filter(slug="ecole").update(status=PublicationStatus.DRAFT)
    result = {t.slug: t.sheet_count for t in services.public_topics()}
    assert len(result) == 9 and "ecole" not in result
    assert result["logement"] == 2
    assert result["sante"] == 0
    assert services.public_topic("ecole") is None
    assert services.public_topic("logement").sheet_count == 2


def test_public_sheet_lookup(topic, sheet_factory):
    sheet = sheet_factory("S", slug="s")
    sheet_factory("Hidden", slug="h", status=PublicationStatus.REVIEW)
    assert services.public_sheet(topic, "s") == sheet
    assert services.public_sheet(topic, "h") is None
    assert services.public_sheet(topic, "nope") is None


def test_workflow_requires_legal_review_then_permission(sheet_factory, staff_user, publisher_user, reviewer):
    sheet = sheet_factory("W", slug="w", status=PublicationStatus.DRAFT, reviewed=False)
    services.submit_for_review(sheet, staff_user)
    assert sheet.status == PublicationStatus.REVIEW
    with pytest.raises(services.WorkflowError):
        services.publish(sheet, publisher_user)  # not legally reviewed yet
    services.mark_reviewed(sheet, reviewer)
    assert sheet.legal_review == LegalReviewStatus.REVIEWED and sheet.reviewer == reviewer
    with pytest.raises(PermissionDenied):
        services.publish(sheet, staff_user)
    services.publish(sheet, publisher_user)
    assert sheet.status == PublicationStatus.PUBLISHED and sheet.published_at is not None
    services.archive(sheet, publisher_user)
    assert sheet.status == PublicationStatus.ARCHIVED
    actions = set(AuditEvent.objects.filter(target_type="LivingSheet").values_list("action", flat=True))
    assert {
        "living.sheet.submitted_for_review",
        "living.sheet.reviewed",
        "living.sheet.published",
        "living.sheet.archived",
    } <= actions


def test_invalid_transitions(sheet_factory, publisher_user):
    sheet = sheet_factory("P", slug="p")
    with pytest.raises(services.WorkflowError):
        services.submit_for_review(sheet, publisher_user)
    with pytest.raises(services.WorkflowError):
        services.publish(sheet, publisher_user)
    draft = sheet_factory("D", slug="d", status=PublicationStatus.DRAFT)
    with pytest.raises(services.WorkflowError):
        services.archive(draft, publisher_user)
