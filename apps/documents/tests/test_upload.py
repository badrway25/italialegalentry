"""Upload hardening: allow-lists, sniffing, size, PDF active content, random names, private storage."""

from __future__ import annotations

from pathlib import Path

import pytest
from django.conf import settings

from audit.models import AuditEvent
from documents import services
from documents.models import DocumentKind, PrivateDocument, ScanStatus
from documents.tests.conftest import MINIMAL_PDF, PDF_WITH_JS, PDF_WITH_LAUNCH, image_bytes, upload_file

pytestmark = [pytest.mark.django_db, pytest.mark.security]

UPLOAD_URL = "/documents/upload/"
INDEX_URL = "/documents/"


def _reason(uploaded):
    with pytest.raises(services.UploadRejected) as exc:
        services.validate_upload(uploaded)
    return exc.value.reason


@pytest.mark.parametrize(
    "name, content",
    [
        ("virus.exe", b"MZ\x90\x00" + b"\x00" * 64),
        ("page.html", b"<html><script>alert(1)</script></html>"),
        ("image.svg", b"<svg xmlns='http://www.w3.org/2000/svg'><script>alert(1)</script></svg>"),
        ("script.js", b"alert(1)"),
        ("archive.zip", b"PK\x03\x04" + b"\x00" * 32),
        ("noext", MINIMAL_PDF),
        ("double.pdf.exe", MINIMAL_PDF),
    ],
)
def test_extension_allowlist(name, content):
    assert _reason(upload_file(name, content)) == "extension"


def test_extension_is_normalised_before_the_allowlist():
    v = services.validate_upload(upload_file("weird.PdF.", MINIMAL_PDF))
    assert v.original_name == "weird.pdf" and v.extension == ".pdf"


@pytest.mark.parametrize(
    "name, content",
    [
        ("fake.pdf", b"MZ\x90\x00 not a pdf at all"),
        ("fake.png", MINIMAL_PDF),
        ("fake.jpg", image_bytes("PNG")),
        ("fake.png", image_bytes("JPEG")),
        ("html.pdf", b"<html>%PDF-1.4</html>"),
    ],
)
def test_content_must_match_extension(name, content):
    assert _reason(upload_file(name, content, "application/pdf")) == "content_mismatch"


def test_client_content_type_is_ignored():
    assert _reason(upload_file("evil.pdf", b"<script>", "application/pdf")) == "content_mismatch"
    assert _reason(upload_file("evil.exe", MINIMAL_PDF, "application/pdf")) == "extension"


def test_oversize_and_empty():
    big = upload_file("big.pdf", MINIMAL_PDF + b"0" * (services.MAX_UPLOAD_BYTES + 1))
    assert _reason(big) == "too_large"
    assert _reason(upload_file("empty.pdf", b"")) == "empty"


def test_pdf_with_active_content_rejected():
    assert _reason(upload_file("js.pdf", PDF_WITH_JS)) == "pdf_active_content"
    assert _reason(upload_file("launch.pdf", PDF_WITH_LAUNCH)) == "pdf_active_content"
    assert _reason(upload_file("js2.pdf", MINIMAL_PDF + b"\n<</S/JavaScript>>")) == "pdf_active_content"


def test_corrupt_image_rejected():
    truncated = image_bytes("PNG")[:40]
    assert _reason(upload_file("broken.png", truncated)) == "image_invalid"


def test_valid_files_are_accepted(pdf_file, png_file, jpeg_file):
    v = services.validate_upload(pdf_file)
    assert (v.extension, v.content_type, v.original_name) == (".pdf", "application/pdf", "Contrat de travail.pdf")
    assert len(v.sha256) == 64
    assert services.validate_upload(png_file).content_type == "image/png"
    v = services.validate_upload(jpeg_file)
    assert v.content_type == "image/jpeg" and v.original_name == "scan.jpg"


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("../../etc/passwd.pdf", "passwd.pdf"),
        ("C:\\Users\\x\\..\\secret.PDF", "secret.pdf"),
        ("  .hidden.pdf", "hidden.pdf"),
        ("a\x00b\r\n.png", "ab.png"),
        ("<script>.jpg", "script.jpg"),
        ("<script>alert(1)</script>.jpg", "script.jpg"),
        ("<b>bold</b>name.png", "b_name.png"),
        ("", "document"),
        ("x" * 300 + ".pdf", "x" * 100 + ".pdf"),
        ("Dossier N°12 — été.pdf", "Dossier N_12 _ été.pdf"),
    ],
)
def test_sanitise_filename(raw, expected):
    assert services.sanitise_filename(raw) == expected


def test_store_upload_uses_random_name_under_private_root(owner, pdf_file):
    doc = services.store_upload(owner, pdf_file, DocumentKind.CONTRACT, "  contrat  ")
    assert doc.original_name == "Contrat de travail.pdf"
    assert doc.stored_name != doc.original_name
    assert doc.stored_name.endswith(".pdf") and len(doc.stored_name) == 36
    # No scanner is deployed in this configuration, and the row says exactly that rather than
    # claiming an analysis is queued (documents.models.ScanStatus.NOT_CONFIGURED).
    assert doc.scan_status == ScanStatus.NOT_CONFIGURED
    assert doc.scanned_at is None
    assert doc.content_type == "application/pdf" and doc.size == len(MINIMAL_PDF)
    assert doc.description == "  contrat  "[:200]
    private_root = Path(settings.PRIVATE_MEDIA_ROOT).resolve()
    media_root = Path(settings.MEDIA_ROOT).resolve()
    stored = private_root / str(owner.pk) / doc.stored_name
    assert stored.exists() and stored.read_bytes() == MINIMAL_PDF
    assert media_root not in stored.parents
    assert not media_root.exists() or not any(media_root.rglob(doc.stored_name))
    event = AuditEvent.objects.get(action="documents.uploaded")
    assert event.target_id == str(doc.pk) and event.actor_id == owner.pk


def test_two_uploads_of_same_file_get_distinct_names(owner):
    a = services.store_upload(owner, upload_file("a.pdf", MINIMAL_PDF), DocumentKind.OTHER)
    b = services.store_upload(owner, upload_file("a.pdf", MINIMAL_PDF), DocumentKind.OTHER)
    assert a.stored_name != b.stored_name and a.sha256 == b.sha256


def test_private_storage_refuses_media_root(settings):
    from django.core.exceptions import ImproperlyConfigured

    from documents.storage import private_storage

    settings.PRIVATE_MEDIA_ROOT = Path(settings.MEDIA_ROOT) / "private"
    with pytest.raises(ImproperlyConfigured):
        private_storage()


def test_private_file_is_not_served_under_media(client, owner, pdf_file):
    doc = services.store_upload(owner, pdf_file, DocumentKind.OTHER)
    client.force_login(owner)
    for url in (f"/media/{owner.pk}/{doc.stored_name}", f"/media/private/{owner.pk}/{doc.stored_name}"):
        assert client.get(url).status_code == 404
    assert client.get(f"/static/{owner.pk}/{doc.stored_name}").status_code == 404


def test_scanner_hook_default_and_pluggable(settings, tmp_path):
    path = tmp_path / "x.pdf"
    path.write_bytes(MINIMAL_PDF)
    assert services.scan_file(str(path)) == "not_configured", "no scanner must never read as 'pending'"
    settings.DOCUMENT_SCANNER = "documents.tests.test_upload.fake_infected_scanner"
    assert services.scan_file(str(path)) == "infected"
    settings.DOCUMENT_SCANNER = "documents.tests.test_upload.fake_broken_scanner"
    assert services.scan_file(str(path)) == "error"
    settings.DOCUMENT_SCANNER = "documents.tests.test_upload.fake_weird_scanner"
    assert services.scan_file(str(path)) == "error"


def fake_infected_scanner(path):
    return "infected"


def fake_clean_scanner(path):
    return "clean"


def fake_broken_scanner(path):
    raise RuntimeError("scanner down")


def fake_weird_scanner(path):
    return "ok"


def test_infected_upload_is_kept_as_record_but_file_removed(settings, owner, pdf_file):
    settings.DOCUMENT_SCANNER = "documents.tests.test_upload.fake_infected_scanner"
    doc = services.store_upload(owner, pdf_file, DocumentKind.OTHER)
    assert doc.scan_status == ScanStatus.INFECTED
    assert doc.file_removed_at is not None
    assert not (Path(settings.PRIVATE_MEDIA_ROOT) / str(owner.pk) / doc.stored_name).exists()


# ---------------------------------------------------------------------------------------------
# Upload view
# ---------------------------------------------------------------------------------------------
def test_upload_view_requires_login(client):
    r = client.get(UPLOAD_URL)
    assert r.status_code == 302 and "/compte/login/" in r["Location"]


def test_upload_view_requires_accepted_terms(client, user_factory):
    user = user_factory("noterms@example.test")
    client.force_login(user)
    r = client.get(UPLOAD_URL)
    assert r.status_code == 403
    assert "Dépôt indisponible" in r.content.decode()
    r = client.post(UPLOAD_URL, {"file": upload_file("a.pdf", MINIMAL_PDF), "kind": "other"})
    assert r.status_code == 403
    assert PrivateDocument.objects.count() == 0


def test_upload_view_happy_path_and_listing(client, owner, organisation, user_factory):
    from accounts.models import Membership, MembershipRole

    Membership.objects.create(user=owner, organisation=organisation, role=MembershipRole.MEMBER)
    client.force_login(owner)
    assert client.get(UPLOAD_URL).status_code == 200
    r = client.post(
        UPLOAD_URL,
        {
            "file": upload_file("Diplôme.pdf", MINIMAL_PDF, "application/pdf"),
            "kind": "diploma",
            "description": "Licence",
            "organisation": organisation.pk,
        },
    )
    assert r.status_code == 302 and r["Location"].endswith(INDEX_URL)
    doc = PrivateDocument.objects.get()
    assert doc.owner == owner and doc.kind == "diploma" and doc.organisation == organisation
    assert doc.uploaded_ip_hash != ""
    html = client.get(INDEX_URL).content.decode()
    # A file that answers no requirement is listed under "Autres fichiers déposés", demoted below
    # the register and named for what it is.
    assert "Autres fichiers déposés" in html
    assert "Diplôme.pdf" in html
    assert doc.stored_name not in html, "the random stored name is never exposed"
    assert f"/documents/{doc.pk}/delete/" in html, "a loose file stays the account's to remove"


def test_upload_view_rejects_bad_file_without_saving(client, owner):
    client.force_login(owner)
    r = client.post(UPLOAD_URL, {"file": upload_file("evil.html", b"<script>"), "kind": "other"})
    assert r.status_code == 200
    assert "Format non accept" in r.content.decode()
    assert PrivateDocument.objects.count() == 0
    r = client.post(UPLOAD_URL, {"file": upload_file("js.pdf", PDF_WITH_JS), "kind": "other"})
    assert r.status_code == 200 and PrivateDocument.objects.count() == 0


def test_upload_cannot_attach_foreign_organisation(client, owner, organisation):
    """Owner is not a member of `organisation` here: the choice must be rejected."""
    client.force_login(owner)
    r = client.post(
        UPLOAD_URL,
        {"file": upload_file("a.pdf", MINIMAL_PDF), "kind": "other", "organisation": organisation.pk},
    )
    assert r.status_code == 200 and PrivateDocument.objects.count() == 0


def test_upload_view_is_throttled(client, owner, settings):
    from core import throttle
    from documents import views

    client.force_login(owner)
    limit = views.UPLOAD_THROTTLE["limit"]
    for _ in range(limit):
        assert throttle.allow(client.request().wsgi_request, "documents_upload", **views.UPLOAD_THROTTLE)
    r = client.post(UPLOAD_URL, {"file": upload_file("a.pdf", MINIMAL_PDF), "kind": "other"})
    assert r.status_code == 429
    assert PrivateDocument.objects.count() == 0
