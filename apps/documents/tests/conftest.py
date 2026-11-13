# ruff: noqa: F811 — pytest fixtures legitimately shadow the imported shared fixture names
from __future__ import annotations

import io

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from accounts import roles
from accounts.models import Membership, MembershipRole, Organisation, OrganisationKind
from core import clock

# Shared project fixtures (tests/conftest.py is not a root conftest, so import them explicitly).
from tests.conftest import (  # noqa: F401
    _clear_caches,
    legal_published,
    person_user,
    seeded,
    set_flag,
    staff_user,
    superuser,
    url,
    user_factory,
)

MINIMAL_PDF = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\n"
    b"trailer<</Root 1 0 R>>\n%%EOF\n"
)
PDF_WITH_JS = MINIMAL_PDF.replace(b"/Type/Catalog", b"/Type/Catalog/OpenAction<</S/JavaScript/JS(app.alert(1))>>")
PDF_WITH_LAUNCH = MINIMAL_PDF.replace(b"/Type/Catalog", b"/Type/Catalog/OpenAction<</S/Launch/F(cmd.exe)>>")


def image_bytes(fmt: str, size=(8, 8)) -> bytes:
    buf = io.BytesIO()
    Image.new("RGB", size, color=(30, 60, 120)).save(buf, format=fmt)
    return buf.getvalue()


def upload_file(name: str, content: bytes, content_type: str = "application/octet-stream") -> SimpleUploadedFile:
    return SimpleUploadedFile(name, content, content_type=content_type)


@pytest.fixture(autouse=True)
def _private_root(settings, tmp_path):
    settings.PRIVATE_MEDIA_ROOT = tmp_path / "private"
    settings.MEDIA_ROOT = tmp_path / "media"
    yield


@pytest.fixture
def pdf_file():
    return upload_file("Contrat de travail.pdf", MINIMAL_PDF, "application/pdf")


@pytest.fixture
def png_file():
    return upload_file("photo.png", image_bytes("PNG"), "image/png")


@pytest.fixture
def jpeg_file():
    return upload_file("scan.JPG", image_bytes("JPEG"), "image/jpeg")


@pytest.fixture
def owner(user_factory):
    return user_factory("owner@example.test", role=roles.PERSON, full_name="Owner One", terms_accepted_at=clock.now())


@pytest.fixture
def intruder(user_factory):
    return user_factory("intruder@example.test", role=roles.PERSON, terms_accepted_at=clock.now())


@pytest.fixture
def staff_role_user(user_factory):
    return user_factory("staffrole@example.test", role=roles.STAFF)


@pytest.fixture
def organisation(db, owner):
    return Organisation.objects.create(name="Acme", kind=OrganisationKind.COMPANY, created_by=owner)


@pytest.fixture
def org_owner(user_factory, organisation):
    user = user_factory("orgowner@example.test", role=roles.COMPANY)
    Membership.objects.create(user=user, organisation=organisation, role=MembershipRole.OWNER)
    return user


@pytest.fixture
def org_member(user_factory, organisation):
    user = user_factory("orgmember@example.test", role=roles.COMPANY)
    Membership.objects.create(user=user, organisation=organisation, role=MembershipRole.MEMBER)
    return user


# -------------------------------------------------------------------------------------------
# The case file a document requirement hangs on (documents attach to cases; see cases/models.py)
# -------------------------------------------------------------------------------------------
@pytest.fixture
def case(db, owner):
    from cases.models import CasePurpose
    from cases.services import open_case

    return open_case(owner, purpose=CasePurpose.WORK, pathway_key="salaried_work")


@pytest.fixture
def requirement(db, case):
    """A piece the PERSON must provide — the ordinary case."""
    from cases.models import ResponsibleActor
    from documents import services
    from documents.models import DocumentKind

    return services.declare_requirement(
        case,
        code="identity_document",
        title="Passeport en cours de validité",
        responsible_actor=ResponsibleActor.PERSON,
        kind=DocumentKind.IDENTITY,
        source_title="D.lgs. 286/1998",
        source_ref="art. 4, comma 1",
    )


@pytest.fixture
def authority_requirement(db, case):
    """A piece the AUTHORITY must issue: the applicant cannot file it and must not be offered to."""
    from cases.models import ResponsibleActor
    from documents import services

    return services.declare_requirement(
        case,
        code="nulla_osta",
        title="Nulla osta au travail",
        responsible_actor=ResponsibleActor.AUTHORITY,
        source_title="D.lgs. 286/1998",
        source_ref="art. 22",
    )


@pytest.fixture
def professional(user_factory, case):
    """A live assignee with a mandate that covers acting on the case's pieces."""
    from cases.models import AssignmentRole
    from cases.services import assign

    user = user_factory("pro@example.test", role=roles.PROFESSIONAL, terms_accepted_at=clock.now())
    assign(case, user, role=AssignmentRole.PROFESSIONAL, mandate_note="mandat de test")
    return user


@pytest.fixture
def revoked_professional(user_factory, case):
    """Same mandate, revoked. It must grant nothing at all."""
    from cases.models import AssignmentRole
    from cases.services import assign, revoke_assignment

    user = user_factory("expro@example.test", role=roles.PROFESSIONAL, terms_accepted_at=clock.now())
    revoke_assignment(assign(case, user, role=AssignmentRole.PROFESSIONAL))
    return user


@pytest.fixture
def admin_role_user(user_factory):
    return user_factory("adminrole@example.test", role=roles.ADMINISTRATOR, terms_accepted_at=clock.now())
