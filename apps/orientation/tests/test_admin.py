"""Back-office: pages render, rule validation on save, activation action, anonymised CSV export."""

import json

import pytest
from django.urls import reverse

from orientation import services
from orientation.models import OrientationResult, OrientationSession, Rule, Ruleset, RulesetStatus
from orientation.tests.conftest import walk

pytestmark = pytest.mark.django_db


@pytest.fixture
def admin_client(client, superuser):
    client.force_login(superuser)
    return client


@pytest.fixture
def completed(active_ruleset):
    from django.test import Client

    c = Client()
    url = c.post("/fr/orientation/")["Location"]
    walk(c, url, [("objective", "work"), ("work_profile", "salaried"), ("training_interest", "false")])
    return OrientationSession.objects.get()


@pytest.mark.parametrize(
    "name",
    [
        "orientation_ruleset_changelist",
        "orientation_question_changelist",
        "orientation_choice_changelist",
        "orientation_outcome_changelist",
        "orientation_checklistitem_changelist",
        "orientation_rule_changelist",
        "orientation_orientationsession_changelist",
        "orientation_orientationresult_changelist",
    ],
)
def test_changelists_render(admin_client, completed, name):
    assert admin_client.get(reverse(f"admin:{name}")).status_code == 200


def test_ruleset_change_page_shows_integrity_report_and_pending_note(admin_client, active_ruleset):
    response = admin_client.get(reverse("admin:orientation_ruleset_change", args=[active_ruleset.pk]))
    assert response.status_code == 200
    html = response.content.decode()
    assert "OK —" in html and "CONTENT_PENDING_LEGAL_REVIEW" in html


def test_rule_change_page_shows_readable_conditions(admin_client, active_ruleset):
    rule = active_ruleset.rules.get(name="Travail salarié")
    response = admin_client.get(reverse("admin:orientation_rule_change", args=[rule.pk]))
    assert response.status_code == 200
    import html

    assert "objective = 'work'" in html.unescape(response.content.decode())


def test_rule_form_rejects_invalid_conditions(admin_client, active_ruleset):
    outcome = active_ruleset.outcomes.first()
    data = {
        "ruleset": active_ruleset.pk,
        "order": 999,
        "name": "bad rule",
        "conditions": json.dumps({"question_key": "objective", "op": "eq", "value": "zzz"}),
        "next_question": "",
        "outcome": outcome.pk,
        "explanation_fr": "",
    }
    response = admin_client.post(reverse("admin:orientation_rule_add"), data)
    assert response.status_code == 200
    assert "valeur inconnue" in response.content.decode()
    assert not Rule.objects.filter(name="bad rule").exists()
    data["conditions"] = json.dumps({"question_key": "objective", "op": "eq", "value": "other"})
    response = admin_client.post(reverse("admin:orientation_rule_add"), data)
    assert response.status_code == 302
    assert Rule.objects.filter(name="bad rule").exists()


def test_activate_action_validates_and_swaps(admin_client, active_ruleset, superuser):
    v2 = services.import_ruleset(services.export_ruleset(active_ruleset), version=2, user=superuser)
    url = reverse("admin:orientation_ruleset_changelist")
    response = admin_client.post(url, {"action": "activate_action", "_selected_action": [v2.pk]}, follow=True)
    assert response.status_code == 200
    v2.refresh_from_db()
    active_ruleset.refresh_from_db()
    assert v2.status == RulesetStatus.ACTIVE and active_ruleset.status == RulesetStatus.RETIRED
    broken = Ruleset.objects.create(version=3)
    response = admin_client.post(url, {"action": "activate_action", "_selected_action": [broken.pk]}, follow=True)
    broken.refresh_from_db()
    assert broken.status == RulesetStatus.DRAFT
    assert "Aucune question" in response.content.decode()


def test_validate_and_export_actions(admin_client, active_ruleset):
    url = reverse("admin:orientation_ruleset_changelist")
    response = admin_client.post(
        url, {"action": "validate_action", "_selected_action": [active_ruleset.pk]}, follow=True
    )
    assert "v1: OK" in response.content.decode()
    response = admin_client.post(url, {"action": "export_action", "_selected_action": [active_ruleset.pk]})
    assert response["Content-Type"].startswith("application/json")
    payload = json.loads(response.content)
    assert payload["version"] == 1 and len(payload["questions"]) == 5


def test_results_are_read_only(admin_client, completed):
    result = OrientationResult.objects.get()
    response = admin_client.get(reverse("admin:orientation_orientationresult_change", args=[result.pk]))
    assert response.status_code == 200
    assert 'name="_save"' not in response.content.decode()
    assert admin_client.get(reverse("admin:orientation_orientationresult_add")).status_code == 403


def test_statistics_csv_export_has_no_answers(admin_client, completed):
    result = OrientationResult.objects.get()
    response = admin_client.post(
        reverse("admin:orientation_orientationresult_changelist"),
        {"action": "export_statistics_csv", "_selected_action": [result.pk]},
    )
    assert response["Content-Type"].startswith("text/csv")
    body = response.content.decode()
    assert "salaried_work" in body and "total" in body
    assert "objective" not in body and "work_profile" not in body and str(completed.id) not in body


def test_session_anonymise_action(admin_client, completed):
    response = admin_client.post(
        reverse("admin:orientation_orientationsession_changelist"),
        {"action": "anonymise_action", "_selected_action": [str(completed.pk)]},
        follow=True,
    )
    assert response.status_code == 200
    completed.refresh_from_db()
    assert completed.answers == {} and completed.resume_token_hash == ""


def test_staff_without_permission_gets_403(client, staff_user, active_ruleset):
    client.force_login(staff_user)
    response = client.get(reverse("admin:orientation_ruleset_changelist"))
    assert response.status_code == 403
