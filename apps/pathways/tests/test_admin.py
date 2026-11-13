import pytest

from pathways.models import Pathway

pytestmark = pytest.mark.django_db

CHANGELIST = "/backoffice/pathways/pathway/"


def test_changelist_and_change_form_for_superuser(client, superuser, pathways_seeded):
    client.force_login(superuser)
    r = client.get(CHANGELIST)
    assert r.status_code == 200
    html = r.content.decode()
    assert "Travail salarié" in html
    p = Pathway.objects.get(key="salaried_work")
    r = client.get(f"{CHANGELIST}{p.pk}/change/")
    assert r.status_code == 200
    html = r.content.decode()
    # locked attributes are displayed but never editable
    assert 'name="key"' not in html
    assert 'name="order"' not in html
    assert "Travail salarié" in html
    assert "entrées pour travail dans le cadre des quotas annuels" in html
    # editorial fields and inlines are editable
    assert 'name="eligibility_context_fr"' in html
    assert 'name="steps-0-title_fr"' in html
    assert "CONTENT_PENDING_LEGAL_REVIEW" in html


def test_add_and_delete_are_disabled(client, superuser, pathways_seeded):
    client.force_login(superuser)
    assert client.get(f"{CHANGELIST}add/").status_code == 403
    p = Pathway.objects.get(key="salaried_work")
    assert client.get(f"{CHANGELIST}{p.pk}/delete/").status_code == 403


def test_staff_without_role_gets_no_access(client, staff_user, pathways_seeded):
    client.force_login(staff_user)
    r = client.get(CHANGELIST)
    assert r.status_code in (302, 403)


def test_csv_export_action(client, superuser, pathways_seeded):
    client.force_login(superuser)
    ids = list(Pathway.objects.values_list("pk", flat=True))
    r = client.post(
        CHANGELIST,
        {"action": "export_review_status_csv", "_selected_action": ids, "index": 0},
    )
    assert r.status_code == 200
    assert r["Content-Type"].startswith("text/csv")
    body = r.content.decode("utf-8")
    assert body.splitlines()[0].startswith("order,key,title,status")
    assert "salaried_work" in body and "Travail salarié" in body
    assert len(body.strip().splitlines()) == 9


def test_step_admin_pages(client, superuser, pathways_seeded):
    client.force_login(superuser)
    assert client.get("/backoffice/pathways/pathwaystep/").status_code == 200
    assert client.get("/backoffice/pathways/pathwaydocument/").status_code == 200
    assert client.get("/backoffice/pathways/pathwaywarning/").status_code == 200
    step = Pathway.objects.get(key="salaried_work").steps.first()
    assert client.get(f"/backoffice/pathways/pathwaystep/{step.pk}/change/").status_code == 200
