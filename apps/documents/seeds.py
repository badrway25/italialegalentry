"""
Synthetic register for a case file that already exists, so the seven states can be SEEN working.

Nothing here is real and nothing here is copied from the previous platform: the files are generated
PDFs of one line, the people are the synthetic accounts of the development environment, and the
sources are public legal references anyone can check. No personal data, no scanned identity paper,
no name of a natural person.

The seed is idempotent and additive: it declares a requirement only when its ``code`` is absent
from the case, and never rewrites one an editor or a reviewer has touched. If no case file exists
yet — which is the situation in a fresh test database — it does nothing at all.
"""

from __future__ import annotations

import datetime as dt

from django.core.files.uploadedfile import SimpleUploadedFile

from accounts import roles
from cases.models import CaseFile, ResponsibleActor
from core import clock
from core.seeds import register_seed
from documents.models import AccessClass, DocumentKind, DocumentRequirement, VersionDecision

SEED_MARKER = "seed:documents.register"


#: A one-page PDF built here rather than committed: a binary fixture in the repository is a file
#: nobody reads and everybody trusts.
def _synthetic_pdf(label: str) -> bytes:
    body = f"BT /F1 12 Tf 40 120 Td ({label}) Tj ET".encode("latin-1", "replace")
    return (
        b"%PDF-1.4\n"
        b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
        b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
        b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 300 200]/Contents 4 0 R>>endobj\n"
        b"4 0 obj<</Length " + str(len(body)).encode() + b">>stream\n" + body + b"\nendstream endobj\n"
        b"trailer<</Root 1 0 R>>\n%%EOF\n"
    )


def _upload(label: str) -> SimpleUploadedFile:
    return SimpleUploadedFile(f"{label}.pdf", _synthetic_pdf(label), content_type="application/pdf")


#: (code, title, actor, kind, source title, source reference, access class, detail)
REQUIREMENTS = [
    (
        "identity_document",
        "Passeport en cours de validité",
        ResponsibleActor.PERSON,
        DocumentKind.IDENTITY,
        "D.lgs. 25 luglio 1998, n. 286 — Testo unico sull’immigrazione",
        "art. 4, comma 1",
        AccessClass.RESTRICTED,
        "Pages d’identité uniquement. La validité doit couvrir la durée du séjour envisagé.",
    ),
    (
        "civil_record",
        "Acte d’état civil légalisé",
        ResponsibleActor.PERSON,
        DocumentKind.OTHER,
        "Convention de La Haye du 5 octobre 1961 (apostille)",
        "art. 3",
        AccessClass.RESTRICTED,
        "Traduction assermentée si l’acte n’est pas rédigé dans une langue acceptée.",
    ),
    (
        "criminal_record",
        "Extrait de casier judiciaire",
        ResponsibleActor.PERSON,
        DocumentKind.OTHER,
        "D.P.R. 31 agosto 1999, n. 394",
        "art. 9",
        AccessClass.RESTRICTED,
        "Délivré par l’autorité compétente du pays de résidence.",
    ),
    (
        "diploma",
        "Diplôme ou titre de formation",
        ResponsibleActor.PERSON,
        DocumentKind.DIPLOMA,
        "D.lgs. 286/1998",
        "art. 49 — riconoscimento dei titoli",
        AccessClass.CASE,
        "Copie complète, toutes pages. La déclaration de valeur peut être demandée ensuite.",
    ),
    (
        "language_certificate",
        "Attestation de niveau de langue",
        ResponsibleActor.TRAINING_BODY,
        DocumentKind.DIPLOMA,
        "Quadro comune europeo di riferimento per le lingue (QCER)",
        "Consiglio d’Europa, 2001",
        AccessClass.CASE,
        "Délivrée par l’organisme de formation à l’issue du parcours.",
    ),
    (
        "work_contract",
        "Proposition de contrat de travail",
        ResponsibleActor.COMPANY,
        DocumentKind.CONTRACT,
        "D.lgs. 286/1998",
        "art. 22 — contratto di soggiorno per lavoro subordinato",
        AccessClass.CASE,
        "Établie par l’entreprise. Ce n’est pas une promesse d’embauche ni une garantie de résultat.",
    ),
    (
        "nulla_osta",
        "Nulla osta au travail",
        ResponsibleActor.AUTHORITY,
        DocumentKind.OTHER,
        "D.lgs. 286/1998",
        "art. 22, commi 2-5 — Sportello unico per l’immigrazione",
        AccessClass.CASE,
        "Délivré par le Sportello unico. Cette pièce ne dépend pas de vous.",
    ),
]


def _reviewer():
    """An administrator to stand as the reviewer of the seeded decisions, or nobody."""
    from django.contrib.auth import get_user_model

    User = get_user_model()
    admin = User.objects.filter(is_superuser=True, is_active=True).order_by("pk").first()
    if admin is not None:
        return admin
    for user in User.objects.filter(is_active=True).order_by("pk"):
        if roles.has_role(user, roles.ADMINISTRATOR):
            return user
    return None


@register_seed("documents.register", order=95)
def seed_document_register():
    """Declare the seven requirements on the first active case file and file synthetic versions."""
    from documents import services

    case = CaseFile.objects.active().order_by("created_at").first()
    if case is None:
        return "no case file: nothing seeded"

    created = 0
    for order, (code, title, actor, kind, source_title, source_ref, access, detail) in enumerate(REQUIREMENTS):
        if DocumentRequirement.objects.filter(case=case, code=code).exists():
            continue
        services.declare_requirement(
            case,
            code=code,
            title=title,
            detail=detail,
            responsible_actor=actor,
            kind=kind,
            source_title=source_title,
            source_ref=source_ref,
            access_class=access,
            due_date=clock.today() + dt.timedelta(days=30 + order * 15),
            order=order,
        )
        created += 1

    if not created:
        return "document register already seeded"

    filed = _file_synthetic_versions(case, services)
    return f"{created} requirement(s) declared on case {case.reference}, {filed} version(s) filed"


def _file_synthetic_versions(case, services) -> int:
    """
    Put the register into a state where all seven words are visible on one screen.

    Filing goes through ``store_upload`` like every other deposit — same allow-list, same magic
    bytes, same random storage key — so what is seeded is indistinguishable from what a person
    would deposit, except that the contents are one line of generated text.
    """
    person = case.person
    reviewer = _reviewer()
    today = clock.today()
    plan = [
        # code, expiry, decision, note — one row per visible state
        ("identity_document", today + dt.timedelta(days=720), VersionDecision.ACCEPTED, ""),
        ("civil_record", today + dt.timedelta(days=15), VersionDecision.ACCEPTED, ""),
        ("criminal_record", today - dt.timedelta(days=10), VersionDecision.ACCEPTED, ""),
        (
            "diploma",
            None,
            VersionDecision.REFUSED,
            "Copie partielle : il manque la page portant la mention et la signature.",
        ),
        ("language_certificate", None, VersionDecision.IN_REVIEW, ""),
        ("work_contract", None, VersionDecision.PENDING, ""),
        # nulla_osta is left MANQUANT on purpose: it is the authority's to issue, not the person's.
    ]
    filed = 0
    for code, expires_on, decision, note in plan:
        requirement = DocumentRequirement.objects.filter(case=case, code=code).first()
        if requirement is None or requirement.versions.exists():
            continue
        document = services.store_upload(person, _upload(code), requirement.kind, requirement.title[:200])
        version = requirement.versions.create(
            number=1,
            document=document,
            filed_by=person,
            is_current=True,
            expires_on=expires_on,
        )
        if decision != VersionDecision.PENDING and reviewer is not None:
            services.set_decision(version, decision, actor=reviewer, note=note)
        else:
            services.refresh_state(requirement)
        filed += 1
    return filed
