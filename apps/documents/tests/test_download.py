"""Download authorisation: IDOR, anonymous, staff, organisation owner, scan status, headers, audit."""

from __future__ import annotations

import re
import uuid

import pytest

from audit.models import AuditEvent
from documents import services
from documents.models import DocumentKind, ScanStatus
from documents.tests.conftest import MINIMAL_PDF, upload_file

pytestmark = [pytest.mark.django_db, pytest.mark.security]


def _url(doc):
    return f"/documents/{doc.pk}/"


@pytest.fixture
def doc(owner, pdf_file):
    return services.store_upload(owner, pdf_file, DocumentKind.CONTRACT, "contrat")


@pytest.fixture
def clean_doc(doc):
    services.apply_scan_result(doc, ScanStatus.CLEAN, note="test")
    return doc


def test_anonymous_redirected_to_login(client, doc):
    r = client.get(_url(doc))
    assert r.status_code == 302 and "/compte/login/" in r["Location"]


def test_owner_can_download_with_hardened_headers(client, owner, doc):
    client.force_login(owner)
    r = client.get(_url(doc))
    assert r.status_code == 200
    assert r["Content-Disposition"].startswith("attachment;")
    assert (
        "Contrat de travail.pdf" in r["Content-Disposition"] or "Contrat%20de%20travail.pdf" in r["Content-Disposition"]
    )
    assert r["Content-Type"] == "application/pdf"
    assert r["X-Content-Type-Options"] == "nosniff"
    cache_control = {token.strip() for token in r["Cache-Control"].split(",")}
    assert {"private", "no-store"} <= cache_control
    assert r["X-Frame-Options"] == "DENY"
    assert b"".join(r.streaming_content) == MINIMAL_PDF
    event = AuditEvent.objects.get(action="documents.downloaded")
    assert event.actor_id == owner.pk and event.target_id == str(doc.pk)


def test_idor_other_user_gets_403_even_with_uuid(client, intruder, clean_doc):
    client.force_login(intruder)
    r = client.get(_url(clean_doc))
    assert r.status_code == 403
    assert not AuditEvent.objects.filter(action="documents.downloaded").exists()


def test_unknown_uuid_is_404(client, owner):
    client.force_login(owner)
    assert client.get(f"/documents/{uuid.uuid4()}/").status_code == 404


def test_staff_role_can_download_clean_only(client, staff_role_user, doc):
    client.force_login(staff_role_user)
    assert client.get(_url(doc)).status_code == 403, "pending: owner only"
    services.apply_scan_result(doc, ScanStatus.CLEAN, note="test")
    assert client.get(_url(doc)).status_code == 200


def test_administrator_role_and_superuser(client, user_factory, superuser, clean_doc):
    from accounts import roles

    admin_role = user_factory("adminrole@example.test", role=roles.ADMINISTRATOR)
    client.force_login(admin_role)
    assert client.get(_url(clean_doc)).status_code == 200
    client.force_login(superuser)
    assert client.get(_url(clean_doc)).status_code == 200


def test_moderator_and_plain_backoffice_flag_are_not_enough(client, user_factory, clean_doc):
    from accounts import roles

    moderator = user_factory("mod@example.test", role=roles.MODERATOR)
    client.force_login(moderator)
    assert client.get(_url(clean_doc)).status_code == 403
    flag_only = user_factory("isstaff@example.test", is_staff=True)
    client.force_login(flag_only)
    assert client.get(_url(clean_doc)).status_code == 403, "is_staff alone grants nothing (RBAC)"


def test_organisation_owner_can_download_member_cannot(client, owner, organisation, org_owner, org_member, pdf_file):
    doc = services.store_upload(owner, pdf_file, DocumentKind.OTHER, organisation=organisation)
    services.apply_scan_result(doc, ScanStatus.CLEAN, note="test")
    client.force_login(org_owner)
    assert client.get(_url(doc)).status_code == 200
    client.force_login(org_member)
    assert client.get(_url(doc)).status_code == 403


def test_infected_never_downloadable(client, owner, superuser, doc):
    services.apply_scan_result(doc, ScanStatus.INFECTED, note="test")
    for user in (owner, superuser):
        client.force_login(user)
        assert client.get(_url(doc)).status_code == 403


def test_soft_delete_hides_document(client, owner, intruder, clean_doc):
    client.force_login(intruder)
    assert client.post(f"/documents/{clean_doc.pk}/delete/").status_code == 403
    client.force_login(owner)
    assert client.get(f"/documents/{clean_doc.pk}/delete/").status_code == 405
    r = client.post(f"/documents/{clean_doc.pk}/delete/")
    assert r.status_code == 302
    clean_doc.refresh_from_db()
    assert clean_doc.deleted_at is not None
    assert client.get(_url(clean_doc)).status_code == 404
    assert clean_doc.original_name not in client.get("/documents/").content.decode()
    assert AuditEvent.objects.filter(action="documents.deleted", target_id=str(clean_doc.pk)).exists()
    client.force_login(owner)
    assert client.post(f"/documents/{clean_doc.pk}/delete/").status_code == 404


def test_index_lists_only_own_documents(client, owner, intruder, pdf_file):
    services.store_upload(owner, pdf_file, DocumentKind.OTHER, "secret-owner-doc")
    client.force_login(intruder)
    html = client.get("/documents/").content.decode()
    assert "secret-owner-doc" not in html and "Contrat de travail" not in html
    # The page is a register of what a case still needs, not a file browser: with no requirement
    # and no file of one's own, it says so in one sentence rather than drawing an empty box.
    assert "Aucune pièce ne vous est demandée" in html


def test_both_delivery_routes_are_rate_bounded(client, owner, monkeypatch):
    """
    The 120/hour bound exists so a compromised session cannot sweep a case file unnoticed. It was
    on the signed route only, which made it decorative: the direct URL was the way round it.
    """
    from documents import views

    monkeypatch.setitem(views.DOWNLOAD_THROTTLE, "limit", 2)
    doc = services.store_upload(owner, upload_file("a.pdf", MINIMAL_PDF), DocumentKind.OTHER)
    client.force_login(owner)
    assert client.get(f"/documents/{doc.pk}/").status_code == 200
    assert client.get(f"/documents/{doc.pk}/").status_code == 200
    assert client.get(f"/documents/{doc.pk}/").status_code == 429
    # And the signed route shares the same counter rather than offering a fresh allowance.
    token = services.signed_download_token(doc, owner)
    assert client.get(f"/documents/link/{token}/").status_code == 429


# --- A row whose stored file is gone (RC v2.0.0, SMOKE D1) -----------------------------------------------------


def _lose_the_file(doc):
    from documents.storage import private_storage

    private_storage().delete(doc.relative_path)
    assert not private_storage().exists(doc.relative_path)


def _missing_records(caplog):
    return [
        r for r in caplog.records if r.name == "ile.documents" and r.getMessage().startswith("documents.file_missing")
    ]


def _without_per_request_tokens(html: bytes) -> bytes:
    """The masked CSRF token and the CSP nonce change on every response; nothing else may."""
    return re.sub(rb'(name="csrfmiddlewaretoken" value|nonce)="[^"]*"', rb'\1=""', html)


def test_a_missing_file_is_a_404_for_the_owner_logged_with_the_id_only(client, owner, doc, caplog):
    """A lost file was an unhandled FileNotFoundError, a 500. Now a 404, one warning, the id and nothing else."""
    _lose_the_file(doc)
    client.force_login(owner)
    with caplog.at_level("WARNING", logger="ile.documents"):
        r = client.get(_url(doc))
    assert r.status_code == 404
    [record] = _missing_records(caplog)
    assert record.levelname == "WARNING"
    assert record.getMessage() == f"documents.file_missing document={doc.pk}"
    for private in (doc.original_name, doc.relative_path, owner.email):
        assert private not in record.getMessage()
    assert not AuditEvent.objects.filter(action="documents.downloaded").exists()


def test_a_missing_file_is_a_404_on_the_signed_route_too(client, owner, doc, caplog):
    _lose_the_file(doc)
    client.force_login(owner)
    token = services.signed_download_token(doc, owner)
    with caplog.at_level("WARNING", logger="ile.documents"):
        assert client.get(f"/documents/link/{token}/").status_code == 404
    assert len(_missing_records(caplog)) == 1


def test_a_missing_file_tells_a_refused_account_nothing(client, intruder, clean_doc, caplog):
    """DENY as strong as ALLOW: the gates run before the file is opened, so a refused account gets the same 403
    whether the file exists or not, and its request writes no file_missing record."""
    client.force_login(intruder)
    before = client.get(_url(clean_doc))
    _lose_the_file(clean_doc)
    with caplog.at_level("WARNING", logger="ile.documents"):
        after = client.get(_url(clean_doc))
    assert before.status_code == after.status_code == 403
    assert _without_per_request_tokens(before.content) == _without_per_request_tokens(after.content)
    assert _missing_records(caplog) == []


def test_a_missing_file_does_not_bypass_the_delivery_gate(client, owner, doc, caplog):
    """The owner may read an infected file's row but never receive it: still a 403, not a 404, when it is gone."""
    services.apply_scan_result(doc, ScanStatus.INFECTED, note="test")
    _lose_the_file(doc)
    client.force_login(owner)
    with caplog.at_level("WARNING", logger="ile.documents"):
        assert client.get(_url(doc)).status_code == 403
    assert _missing_records(caplog) == []


def test_a_missing_file_still_sends_the_anonymous_to_the_sign_in(client, doc):
    _lose_the_file(doc)
    r = client.get(_url(doc))
    assert r.status_code == 302 and "/compte/login/" in r["Location"]
