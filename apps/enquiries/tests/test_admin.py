"""Back-office: read-only data, CSV/JSON exports, mark handled, anonymise."""

import csv
import io
import json

import pytest

from audit.models import AuditEvent
from enquiries.models import ANONYMISED, CompanyNeedsRequest, SubmissionStatus

pytestmark = pytest.mark.django_db

CHANGELIST = "/backoffice/enquiries/companyneedsrequest/"


def _action(client, action, pks):
    return client.post(CHANGELIST, {"action": action, "_selected_action": [str(pk) for pk in pks], "index": "0"})


def test_changelist_and_change_form_are_readonly_for_data(client, superuser, make_company):
    client.force_login(superuser)
    obj = make_company(email="ro@example.test")
    assert client.get(CHANGELIST).status_code == 200
    r = client.get(f"{CHANGELIST}{obj.pk}/change/")
    assert r.status_code == 200
    html = r.content.decode()
    assert 'name="company_name"' not in html  # submission data is not editable
    assert 'name="status"' in html and 'name="admin_notes"' in html
    assert client.get(f"{CHANGELIST}add/").status_code == 403


def test_export_csv_with_bom_and_consent_columns(client, superuser, make_company):
    client.force_login(superuser)
    a = make_company(email="csv1@example.test")
    b = make_company(email="csv2@example.test", company_name="Beta S.r.l.")
    r = _action(client, "export_csv", [a.pk, b.pk])
    assert r.status_code == 200
    assert r["Content-Type"].startswith("text/csv")
    raw = r.content
    assert raw[:3] == bytes([0xEF, 0xBB, 0xBF])  # UTF-8 BOM
    rows = list(csv.reader(io.StringIO(raw.decode("utf-8-sig")), delimiter=";"))
    header, data = rows[0], rows[1:]
    for col in (
        "id",
        "status",
        "company_name",
        "email",
        "consent_text_key",
        "consent_text_version",
        "consent_given_at",
    ):
        assert col in header, col
    assert len(data) == 2
    emails = {row[header.index("email")] for row in data}
    assert emails == {"csv1@example.test", "csv2@example.test"}
    assert {row[header.index("consent_text_key")] for row in data} == {"p1.companies.form.consent"}
    assert all(row[header.index("consent_given_at")] for row in data)
    assert AuditEvent.objects.filter(action="enquiries.export_csv").exists()


def test_export_json_single(client, superuser, make_company):
    client.force_login(superuser)
    a = make_company(email="json@example.test")
    b = make_company(email="json2@example.test")
    r = _action(client, "export_json_single", [a.pk])
    assert r.status_code == 200 and r["Content-Type"].startswith("application/json")
    payload = json.loads(r.content.decode())
    assert payload["email"] == "json@example.test"
    assert AuditEvent.objects.filter(action="enquiries.export_json", target_id=str(a.pk)).exists()
    # more than one selected → refused
    r = _action(client, "export_json_single", [a.pk, b.pk])
    assert r.status_code == 302  # back to the changelist with an error message


def test_mark_handled_action(client, superuser, make_company):
    client.force_login(superuser)
    obj = make_company()
    r = _action(client, "mark_handled", [obj.pk])
    assert r.status_code == 302
    obj.refresh_from_db()
    assert obj.status == SubmissionStatus.HANDLED
    assert obj.handled_by == superuser


def test_anonymise_action(client, superuser, make_company):
    client.force_login(superuser)
    obj = make_company(email="gdpr@example.test")
    r = _action(client, "anonymise_selected", [obj.pk])
    assert r.status_code == 302
    obj.refresh_from_db()
    assert obj.email == ANONYMISED and obj.is_anonymised
    assert CompanyNeedsRequest.objects.filter(email="gdpr@example.test").count() == 0
    assert AuditEvent.objects.filter(action="enquiries.anonymised", target_id=str(obj.pk)).exists()


def test_staff_role_can_open_changelist(client, staff_user, seeded, make_company):
    make_company()
    client.force_login(staff_user)
    assert client.get(CHANGELIST).status_code == 200
