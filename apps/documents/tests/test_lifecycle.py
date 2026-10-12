"""Purge command, scan command, anonymisation hook, admin listing, export section, compliance."""

from __future__ import annotations

import datetime as dt
import re
from io import StringIO
from pathlib import Path

import pytest
from django.conf import settings
from django.core.management import call_command

from accounts import services as account_services
from audit.models import AuditEvent
from cms import locked_content
from cms.forbidden import scan
from documents import services
from documents.models import DocumentKind, PrivateDocument, ScanStatus
from documents.tests.conftest import MINIMAL_PDF, upload_file

pytestmark = [pytest.mark.django_db]


def _path(doc) -> Path:
    return Path(settings.PRIVATE_MEDIA_ROOT) / str(doc.owner_id) / doc.stored_name


def test_purge_expired_is_dry_run_by_default(owner):
    doc = services.store_upload(owner, upload_file("a.pdf", MINIMAL_PDF), DocumentKind.OTHER)
    doc.retention_until = dt.date(2020, 1, 1)
    doc.save()
    out = StringIO()
    call_command("documents_purge_expired", stdout=out)
    assert "would purge (dry-run): 1 expired, 0 soft-deleted" in out.getvalue()
    assert _path(doc).exists()
    call_command("documents_purge_expired", "--apply", stdout=out)
    doc.refresh_from_db()
    assert not _path(doc).exists()
    assert doc.deleted_at is not None and doc.file_removed_at is not None
    assert doc.original_name == "purged" and doc.description == ""
    assert AuditEvent.objects.filter(action="documents.purged", target_id=str(doc.pk)).exists()


def test_purge_removes_files_of_soft_deleted_rows(owner):
    doc = services.store_upload(owner, upload_file("a.pdf", MINIMAL_PDF), DocumentKind.OTHER)
    services.soft_delete(doc)
    assert _path(doc).exists(), "soft delete keeps the file until the purge run"
    counts = services.purge_expired(apply=True)
    assert counts == {"expired": 0, "soft_deleted": 1}
    assert not _path(doc).exists()
    assert services.purge_expired(apply=True) == {"expired": 0, "soft_deleted": 0}


def test_scan_pending_command(settings, owner):
    doc = services.store_upload(owner, upload_file("a.pdf", MINIMAL_PDF), DocumentKind.OTHER)
    out = StringIO()
    call_command("documents_scan_pending", stdout=out)
    assert "not configured" in out.getvalue()
    settings.DOCUMENT_SCANNER = "documents.tests.test_upload.fake_clean_scanner"
    call_command("documents_scan_pending", stdout=out)
    doc.refresh_from_db()
    assert doc.scan_status == ScanStatus.CLEAN and doc.scanned_at is not None
    assert AuditEvent.objects.filter(action="documents.scan_result", target_id=str(doc.pk)).exists()


def test_account_anonymisation_purges_files(owner, intruder):
    mine = services.store_upload(owner, upload_file("a.pdf", MINIMAL_PDF), DocumentKind.IDENTITY)
    theirs = services.store_upload(intruder, upload_file("b.pdf", MINIMAL_PDF), DocumentKind.IDENTITY)
    account_services.anonymise_user(owner, reason="test")
    mine.refresh_from_db()
    theirs.refresh_from_db()
    assert not _path(mine).exists() and mine.deleted_at is not None and mine.original_name == "purged"
    assert _path(theirs).exists() and theirs.deleted_at is None


def test_export_section_lists_own_documents(owner, intruder):
    services.store_upload(owner, upload_file("a.pdf", MINIMAL_PDF), DocumentKind.DIPLOMA, "mine")
    services.store_upload(intruder, upload_file("b.pdf", MINIMAL_PDF), DocumentKind.DIPLOMA, "theirs")
    data = account_services.export_user_data(owner)
    assert [d["description"] for d in data["documents"]] == ["mine"]


def test_hard_delete_removes_file(owner):
    doc = services.store_upload(owner, upload_file("a.pdf", MINIMAL_PDF), DocumentKind.OTHER)
    path = _path(doc)
    assert path.exists()
    doc.delete()
    assert not path.exists()


def test_admin_listing_read_only_and_no_link_for_staff(client, superuser, user_factory, owner):
    from accounts import roles

    doc = services.store_upload(owner, upload_file("a.pdf", MINIMAL_PDF), DocumentKind.OTHER)
    roles.ensure_roles()
    admin_role = user_factory("adm@example.test", role=roles.ADMINISTRATOR, is_staff=True)
    client.force_login(admin_role)
    r = client.get("/backoffice/documents/privatedocument/")
    assert r.status_code == 200
    html = r.content.decode()
    assert f"/documents/{doc.pk}/" not in html
    assert client.get("/backoffice/documents/privatedocument/add/").status_code == 403
    r = client.get(f"/backoffice/documents/privatedocument/{doc.pk}/change/")
    assert r.status_code == 200
    assert f'href="/documents/{doc.pk}/"' not in r.content.decode()
    client.force_login(superuser)
    # No scanner has looked at this file, so ``_serve`` would refuse to deliver it to anybody but
    # its depositor. The back-office therefore prints the RULE, not a link that answers 403.
    html = client.get("/backoffice/documents/privatedocument/").content.decode()
    assert f'href="/documents/{doc.pk}/"' not in html
    assert "Aucun antivirus n’est déployé" in html
    assert client.get(f"/backoffice/documents/privatedocument/{doc.pk}/delete/").status_code == 403
    r = client.post(
        "/backoffice/documents/privatedocument/",
        {"action": "mark_clean", "_selected_action": [str(doc.pk)]},
        follow=True,
    )
    assert r.status_code == 200
    doc.refresh_from_db()
    assert doc.scan_status == ScanStatus.CLEAN
    # The documented manual review is what opens the gate — and then the link is real.
    html = client.get("/backoffice/documents/privatedocument/").content.decode()
    assert f'href="/documents/{doc.pk}/"' in html
    assert client.get(f"/documents/{doc.pk}/").status_code == 200
    r = client.post(
        "/backoffice/documents/privatedocument/",
        {"action": "export_csv", "_selected_action": [str(doc.pk)]},
    )
    assert r.status_code == 200 and r["Content-Type"].startswith("text/csv")
    assert doc.stored_name not in r.content.decode()


def test_str_and_queryset_helpers(owner):
    doc = services.store_upload(owner, upload_file("a.pdf", MINIMAL_PDF), DocumentKind.CONTRACT)
    assert "a.pdf" in str(doc)
    assert doc.relative_path == f"{owner.pk}/{doc.stored_name}"
    assert list(PrivateDocument.objects.pending_scan()) == [doc]
    services.soft_delete(doc)
    assert list(PrivateDocument.objects.alive()) == []
    assert list(PrivateDocument.objects.deleted()) == [doc]


@pytest.mark.compliance
def test_reserved_area_pages_have_no_forbidden_or_handcopied_text(client, owner):
    """Rendered account/document pages: no forbidden formulation, no hand-copied locked text, ™ only."""
    client.force_login(owner)
    pages = ["/documents/", "/documents/upload/", "/fr/compte/profil/", "/fr/compte/profil/suppression/"]
    long_locked = [
        locked_content.canonical(v).strip('"')
        for k, v in locked_content.LOCKED_TEXTS["fr"].items()
        if isinstance(v, str) and len(v) > 25 and not k.startswith("p1.trademark")
    ]
    for url in pages:
        r = client.get(url)
        assert r.status_code == 200, url
        html = r.content.decode()
        assert not scan(html), url
        assert "®" not in html and "Italy Legal Entry™" in html
        assert len(re.findall(r"<h1[\s>]", html)) == 1, url
        assert "<main" in html and "<nav" in html
        assert 'name="robots" content="noindex' in html
        for text in long_locked:
            assert text not in html, (url, text[:40])
        assert not re.search(r'(?:src|href)="https?://(?!testserver)', html), url


@pytest.mark.compliance
def test_templates_do_not_hand_copy_locked_texts():
    base = Path(settings.BASE_DIR) / "templates"
    files = list((base / "accounts").rglob("*.html")) + list((base / "documents").rglob("*.html"))
    assert files
    locked = [v for v in locked_content.LOCKED_TEXTS["fr"].values() if isinstance(v, str) and len(v) > 25]
    for f in files:
        src = f.read_text(encoding="utf-8")
        for text in locked:
            assert text not in src, (f.name, text[:40])
        assert "®" not in src
        assert "@legalitalentry.it" not in src
        assert not re.search(r"\bmatching\b", src, flags=re.IGNORECASE)
