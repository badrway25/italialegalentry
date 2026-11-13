"""Unit tests for enquiries.services and models (hashing, anonymisation, retention, portal hook)."""

import datetime as dt
import json

import pytest
from django.core.management import call_command
from django.utils import timezone

from audit.models import AuditEvent
from enquiries import services
from enquiries.models import (
    ANONYMISED,
    CollaborationProposal,
    CompanyNeedsRequest,
    ContactRequest,
    SubmissionStatus,
    compute_duplicate_hash,
)

pytestmark = pytest.mark.django_db


def test_duplicate_hash_is_normalised_and_model_scoped():
    a = compute_duplicate_hash("enquiries.companyneedsrequest", {"email": "A@X.test", "company_name": "ACME  S.p.A."})
    b = compute_duplicate_hash("enquiries.companyneedsrequest", {"email": "a@x.test ", "company_name": "acme s.p.a."})
    c = compute_duplicate_hash("enquiries.contactrequest", {"email": "a@x.test", "company_name": "acme s.p.a."})
    assert a == b
    assert a != c
    assert len(a) == 64


def test_model_duplicate_key_values_include_email(make_company):
    obj = make_company(email="dup@example.test")
    keys = obj.duplicate_key_values()
    assert set(keys) == {"email", "company_name", "profiles_needed"}
    assert obj.duplicate_hash == obj.compute_duplicate_hash()


def test_data_rows_use_field_labels(make_company):
    obj = make_company()
    rows = obj.data_rows()
    assert len(rows) == 14
    assert rows[0] == (str(CompanyNeedsRequest._meta.get_field("company_name").verbose_name), "ACME S.p.A.")


def test_anonymise_replaces_personal_fields_and_audits(make_company, person_user):
    obj = make_company(email="erase@example.test", owner=person_user, notes="private note")
    services.anonymise(obj, user=person_user, reason="test")
    obj.refresh_from_db()
    assert obj.is_anonymised
    assert obj.email == ANONYMISED
    assert obj.contact_name_and_role == ANONYMISED
    assert obj.phone == ANONYMISED
    assert obj.notes == ANONYMISED
    assert obj.company_name == "ACME S.p.A."  # organisation data is not personal data
    assert obj.owner is None
    assert obj.ip_hash == "" and obj.user_agent == "" and obj.duplicate_hash == ""
    event = AuditEvent.objects.get(action="enquiries.anonymised")
    assert event.target_id == str(obj.pk)
    assert event.metadata["fields"] == list(CompanyNeedsRequest.PERSONAL_FIELDS)
    # idempotent
    services.anonymise(obj)
    assert AuditEvent.objects.filter(action="enquiries.anonymised").count() == 1


def test_anonymise_contact_and_proposal(make_contact, make_proposal):
    c = services.anonymise(make_contact())
    p = services.anonymise(make_proposal())
    assert c.name == ANONYMISED and c.message == ANONYMISED
    assert p.contact_name_and_role == ANONYMISED and p.proposal == ANONYMISED and p.organisation_name == "Regione X"


def test_mark_handled(make_company, staff_user):
    obj = services.mark_handled(make_company(), staff_user)
    obj.refresh_from_db()
    assert obj.status == SubmissionStatus.HANDLED
    assert obj.handled_by == staff_user
    assert obj.handled_at is not None and obj.last_contact_at == obj.handled_at
    assert AuditEvent.objects.filter(action="enquiries.handled", target_id=str(obj.pk)).exists()


def _age(obj, days: int):
    type(obj).objects.filter(pk=obj.pk).update(created_at=timezone.now() - dt.timedelta(days=days))


def test_purge_expired_dry_run_then_apply(make_company, make_contact, make_proposal):
    old = make_company(email="old@example.test")
    _age(old, 800)
    recent = make_company(email="recent@example.test")
    kept_by_contact = make_company(email="kept@example.test")
    _age(kept_by_contact, 800)
    CompanyNeedsRequest.objects.filter(pk=kept_by_contact.pk).update(last_contact_at=timezone.now())
    old_contact = make_contact()
    _age(old_contact, 800)
    _age(make_proposal(), 10)

    counts = services.purge_expired()  # dry-run by default, 24 months from settings
    assert counts == {
        "enquiries.CompanyNeedsRequest": 1,
        "enquiries.CollaborationProposal": 0,
        "enquiries.ContactRequest": 1,
    }
    assert CompanyNeedsRequest.objects.count() == 3
    assert not AuditEvent.objects.filter(action="enquiries.purged").exists()

    counts = services.purge_expired(dry_run=False)
    assert counts["enquiries.CompanyNeedsRequest"] == 1
    assert set(CompanyNeedsRequest.objects.values_list("pk", flat=True)) == {recent.pk, kept_by_contact.pk}
    assert ContactRequest.objects.count() == 0
    assert CollaborationProposal.objects.count() == 1
    event = AuditEvent.objects.get(action="enquiries.purged")
    assert event.metadata["months"] == 24


def test_purge_command_dry_run_default_and_apply(make_company, capsys):
    obj = make_company()
    _age(obj, 800)
    call_command("purge_expired_submissions")
    assert CompanyNeedsRequest.objects.filter(pk=obj.pk).exists()
    assert "DRY-RUN" in capsys.readouterr().out
    call_command("purge_expired_submissions", "--apply", "--months", "12")
    assert not CompanyNeedsRequest.objects.filter(pk=obj.pk).exists()
    assert "APPLIED" in capsys.readouterr().out


def test_submissions_for_user(make_company, make_contact, make_proposal, user_factory):
    a = user_factory("a@example.test")
    b = user_factory("b@example.test")
    c1 = make_company(email="a@example.test", owner=a)
    p1 = make_proposal(email="a@example.test", owner=a)
    make_contact(email="b@example.test", owner=b)
    make_company(email="anon@example.test")
    erased = make_contact(email="a@example.test", owner=a)
    services.anonymise(erased)
    items = services.submissions_for_user(a)
    assert {o.pk for o in items} == {c1.pk, p1.pk}
    assert items == sorted(items, key=lambda o: o.created_at, reverse=True)
    assert services.submissions_for_user(b)[0].email == "b@example.test"

    class Anon:
        is_authenticated = False

    assert services.submissions_for_user(Anon()) == []


def test_export_json_contains_data_and_consent(make_company):
    obj = make_company(email="export@example.test")
    payload = json.loads(services.export_json(obj))
    assert payload["model"] == "enquiries.CompanyNeedsRequest"
    assert payload["email"] == "export@example.test"
    assert payload["consent_text_key"] == "p1.companies.form.consent"
    assert payload["consent_text_version"] == "1"
    assert payload["consent_given_at"]
    assert set(services.export_header(CompanyNeedsRequest)) <= set(payload)


def test_retention_reference_prefers_last_contact(make_company):
    obj = make_company()
    assert obj.retention_reference == obj.created_at
    obj.handled_at = timezone.now()
    assert obj.retention_reference == obj.handled_at
    obj.last_contact_at = timezone.now() + dt.timedelta(days=1)
    assert obj.retention_reference == obj.last_contact_at
