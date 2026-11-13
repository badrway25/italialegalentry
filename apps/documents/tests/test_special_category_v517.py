"""
V5.17 §4–§5 — R-SC-1, the production safety control for special-category data (``core.special_category``).

DENY as strong as ALLOW, both read through the real roads (the piece's page, the register, the form post, the
Dépôt's JSON answer, the service) and the settings modules themselves:

* the switch off (base.py's default, prod.py's): a special-category piece offers no filing, says so calmly, and is
  refused by the view and by the service; the loose upload offers no «Autre document» and refuses it when posted;
* the switch on (the preview, the suite): the same piece is filed and the loose upload keeps every kind;
* an ordinary piece (a passport) stays open either way — the control closes what solicits art. 9 data, nothing else;
* the guidance G-FREE / G-UPLOAD stands under the free texts and the upload, in it/fr/en/ar;
* prod.py holds the switch off, and refuses to switch it on without the written approval's reference (A-31).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from django.utils import translation

from cases.models import ResponsibleActor
from core import special_category
from documents import services
from documents.models import DocumentKind, PrivateDocument
from documents.tests.conftest import MINIMAL_PDF, upload_file

pytestmark = [pytest.mark.django_db, pytest.mark.security]

ROOT = Path(__file__).resolve().parents[3]
UPLOAD_URL = "/documents/upload/"
CLOSED_FR = special_category.CLOSED_PIECE["fr"]


def pdf(name="piece.pdf"):
    return upload_file(name, MINIMAL_PDF, "application/pdf")


@pytest.fixture
def production(settings):
    settings.ILE_SPECIAL_CATEGORY_FLOWS_ENABLED = False


@pytest.fixture
def preview(settings):
    settings.ILE_SPECIAL_CATEGORY_FLOWS_ENABLED = True


@pytest.fixture
def medical_requirement(db, case):
    """A piece that, by what it names, is a special-category document (SPECIAL_CATEGORY_AUDIT S-02)."""
    return services.declare_requirement(
        case,
        code="medical_certificate",
        title="Certificat médical d’aptitude",
        responsible_actor=ResponsibleActor.PERSON,
        kind=DocumentKind.OTHER,
        source_title="Fictional source for the test",
        source_ref="—",
    )


def detail(requirement):
    return f"/documents/requirements/{requirement.pk}/"


def file_url(requirement):
    return f"/documents/requirements/{requirement.pk}/file/"


# --------------------------------------------------------------------------------------------- the classification
@pytest.mark.parametrize(
    "title",
    [
        "Certificat médical d’aptitude",
        "Certificato medico",
        "Medical certificate",
        "Attestation de handicap",
        "Certificat de mariage religieux",
        "Carte syndicale",
        "Relevé d’empreintes digitales",
    ],
)
def test_a_piece_that_names_a_special_category_document_is_recognised(title):
    class Piece:
        code, detail = "piece", ""

    Piece.title = title
    assert special_category.solicits_special_category(Piece)


@pytest.mark.parametrize(
    "title",
    [
        "Passeport en cours de validité",
        "Assurance médicale de voyage",
        "Diplôme ou titre de formation",
        "Proposition de contrat de travail",
        "Acte d’état civil légalisé",
        "Passeport biométrique",
        "Photo d'identité biométrique",
    ],
)
def test_an_ordinary_piece_is_not_closed(title):
    class Piece:
        code, detail = "piece", ""

    Piece.title = title
    assert not special_category.solicits_special_category(Piece)


@pytest.mark.parametrize(
    "detail",
    ["Copie intégrale, sans mention religieuse.", "No health data: the identity page only.", "Senza dati sanitari."],
)
def test_a_detail_that_says_what_not_to_send_does_not_close_the_piece(detail):
    """The guard reads the code and the title, never the detail (a detail often names what NOT to send)."""

    class Piece:
        code, title = "birth_certificate", "Acte de naissance"

    Piece.detail = detail
    assert not special_category.solicits_special_category(Piece)


def test_biometric_data_is_recognised_by_name():
    class Piece:
        code, detail, title = "piece", "", "Relevé de données biométriques"

    assert special_category.solicits_special_category(Piece)


# --------------------------------------------------------------------------------------------- DENY (production)
def test_production_offers_no_filing_for_a_special_category_piece_and_says_so_calmly(
    client, owner, medical_requirement, production
):
    client.force_login(owner)
    body = client.get(detail(medical_requirement)).content.decode()
    assert CLOSED_FR in body
    assert "data-depot-form" not in body and medical_requirement.title in body
    for texts in (special_category.CLOSED_PIECE,):  # a finished sentence, never «work in progress»
        for sentence in texts.values():
            assert not any(word in sentence.lower() for word in ("en cours", "in corso", "in progress", "todo", "?"))
    # RESTATED under V5.20 for the owner's GLOBAL SITE + PLATFORM DESIGN COMPLETION directive of 12 Nov 2026: the V5.32
    # integration review's P2-11 — /documents/ leads to «Mes documents», read there
    landing = client.get("/documents/", follow=True)
    assert landing.redirect_chain == [("/fr/espace-reserve/mes-documents/", 302)] and landing.status_code == 200
    register = landing.content.decode()
    assert file_url(medical_requirement) not in register


def test_production_refuses_the_filing_by_form_post_by_the_depot_and_by_the_service(
    client, owner, medical_requirement, production
):
    client.force_login(owner)
    response = client.post(file_url(medical_requirement), {"file": pdf()})
    assert response.status_code in (302, 403)
    answer = client.post(file_url(medical_requirement), {"file": pdf()}, headers={"X-ILE-Depot": "1"}).json()
    assert answer["answer"] == special_category.REFUSAL_CODE and answer["message"] == CLOSED_FR
    with pytest.raises(services.RequirementRefused):
        services.file_version(medical_requirement, owner, pdf())
    assert medical_requirement.versions.count() == 0
    assert PrivateDocument.objects.count() == 0


def test_a_refused_post_shows_the_closed_sentence_once(client, owner, medical_requirement, production):
    client.force_login(owner)
    body = client.post(file_url(medical_requirement), {"file": pdf()}, follow=True).content.decode()
    assert body.count(CLOSED_FR) == 1


def test_production_loose_upload_offers_only_the_named_kinds_and_refuses_other(client, owner, production):
    client.force_login(owner)
    body = client.get(UPLOAD_URL).content.decode()
    assert 'value="other"' not in body
    for kind in ("identity", "diploma", "contract"):
        assert f'value="{kind}"' in body
    assert special_category.G_UPLOAD["fr"] in body
    response = client.post(UPLOAD_URL, {"file": pdf(), "kind": DocumentKind.OTHER})
    assert response.status_code == 200
    assert PrivateDocument.objects.count() == 0
    client.post(UPLOAD_URL, {"file": pdf(), "kind": DocumentKind.DIPLOMA})
    assert PrivateDocument.objects.filter(kind=DocumentKind.DIPLOMA).count() == 1


def test_production_keeps_an_ordinary_piece_open(client, owner, requirement, production):
    client.force_login(owner)
    body = client.get(detail(requirement)).content.decode()
    assert CLOSED_FR not in body and "data-depot-form" in body
    services.file_version(requirement, owner, pdf())
    assert requirement.versions.count() == 1


# --------------------------------------------------------------------------------------------- ALLOW (preview)
def test_the_preview_offers_and_files_the_same_piece(client, owner, medical_requirement, preview):
    client.force_login(owner)
    body = client.get(detail(medical_requirement)).content.decode()
    assert CLOSED_FR not in body and "data-depot-form" in body
    answer = client.post(file_url(medical_requirement), {"file": pdf()}, headers={"X-ILE-Depot": "1"}).json()
    assert answer["answer"] == "filed"
    assert medical_requirement.versions.count() == 1


def test_the_preview_loose_upload_keeps_every_kind(client, owner, preview):
    client.force_login(owner)
    body = client.get(UPLOAD_URL).content.decode()
    assert 'value="other"' in body
    client.post(UPLOAD_URL, {"file": pdf(), "kind": DocumentKind.OTHER})
    assert PrivateDocument.objects.filter(kind=DocumentKind.OTHER).count() == 1


# --------------------------------------------------------------------------------------------- the guidance
@pytest.mark.parametrize("lang", ["it", "fr", "en", "ar"])
def test_the_guidance_reads_in_the_readers_language_under_free_text_and_upload(lang):
    from documents.forms import DocumentUploadForm
    from helpdesk.forms import MessageForm

    with translation.override(lang):
        assert str(MessageForm().fields["body"].help_text) == special_category.G_FREE[lang]
        assert str(special_category.UPLOAD_GUIDANCE) == special_category.G_UPLOAD[lang]
        assert str(special_category.CLOSED_PIECE_NOTICE) == special_category.CLOSED_PIECE[lang]
        assert DocumentUploadForm is not None
    for texts in (special_category.G_FREE, special_category.G_UPLOAD, special_category.CLOSED_PIECE):
        assert "consent" not in texts["en"].lower()


def test_the_case_files_reason_carries_the_free_text_guidance():
    template = (ROOT / "templates/cases/partials/state_dialog.html").read_bytes().decode("utf-8")
    assert "{{ free_text_guidance }}" in template
    view = (ROOT / "apps/cases/views.py").read_bytes().decode("utf-8")
    assert '"free_text_guidance": special_category.FREE_TEXT_GUIDANCE' in view


# --------------------------------------------------------------------------------------------- the settings modules
def _prod_settings(**extra) -> subprocess.CompletedProcess:
    env = {
        **os.environ,
        "DJANGO_SETTINGS_MODULE": "config.settings.prod",
        "DJANGO_SECRET_KEY": "K" + "aB3xY7zQ9wE2rT5yU8iO1pA4sD6fG0hJ-kL_mN3bV5cX7zQ9wE2rT5yU8iO1pA4s",
        "DJANGO_ALLOWED_HOSTS": "example.com",
        "DJANGO_CSRF_TRUSTED_ORIGINS": "https://example.com",
        "IP_HASH_SALT": "Zq3vN8rT1yW6uI0oP5aS9dF2gH7jK4lX-cV_bN1mQ8wE3rT6",
        "BACKOFFICE_MFA_ENFORCED": "1",
        "SECURE_SSL_REDIRECT": "true",
        "SECURE_HSTS_SECONDS": "31536000",
        "SECURE_HSTS_INCLUDE_SUBDOMAINS": "0",
        "SECURE_HSTS_PRELOAD": "0",
        "EMAIL_BACKEND": "django.core.mail.backends.smtp.EmailBackend",
        "EMAIL_HOST": "smtp.example.com",
        "DATABASE_URL": os.environ.get("DATABASE_URL", "postgres://ile:placeholder@127.0.0.1:5432/ile"),
        "DJANGO_DEBUG": "1",  # the preview's DEBUG never reaches the switch in production
        **extra,
    }
    for name in ("ILE_SPECIAL_CATEGORY_FLOWS_ENABLED", "ILE_SPECIAL_CATEGORY_BASIS_REFERENCE"):
        if name not in extra:
            env.pop(name, None)
    code = (
        "import django, json; django.setup(); from django.conf import settings; "
        "from core import special_category; "
        "print(json.dumps([settings.ILE_SPECIAL_CATEGORY_FLOWS_ENABLED, special_category.flows_enabled()]))"
    )
    return subprocess.run(
        [sys.executable, "-c", code], cwd=ROOT, env=env, capture_output=True, text=True, timeout=120, check=False
    )


def test_prod_settings_hold_the_special_category_flows_closed():
    result = _prod_settings()
    assert result.returncode == 0, result.stderr[-800:]
    assert json.loads(result.stdout.strip().splitlines()[-1]) == [False, False]


def test_prod_settings_refuse_to_open_them_without_the_written_approval():
    result = _prod_settings(ILE_SPECIAL_CATEGORY_FLOWS_ENABLED="1")
    assert result.returncode != 0
    assert "ILE_SPECIAL_CATEGORY_BASIS_REFERENCE" in result.stderr


def test_prod_settings_open_them_only_with_the_approvals_reference():
    result = _prod_settings(ILE_SPECIAL_CATEGORY_FLOWS_ENABLED="1", ILE_SPECIAL_CATEGORY_BASIS_REFERENCE="ref-test")
    assert result.returncode == 0, result.stderr[-800:]
    assert json.loads(result.stdout.strip().splitlines()[-1]) == [True, True]


def test_base_settings_default_is_closed():
    base = (ROOT / "config/settings/base.py").read_bytes().decode("utf-8")
    assert "\nILE_SPECIAL_CATEGORY_FLOWS_ENABLED = False\n" in base
