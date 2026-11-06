"""
The preview's data, made fit for the owner's acceptance (V5.12 §11–§13; Director's decisions §8 «Preview data: CLEAN»,
§9; LANE_D audit D-03, D-09, D-19). DEVELOPMENT ONLY.

The owner approves the product on the preview's database (``ile_v5``, served on 8780) and its lane clones. Those rows
were written by fixtures, by QA passes and by a red team, and they spoke like it: «Personne de test QA», «qa-company»,
«Demo — Cantiere Adriatico S.r.l. (entreprise fictive)», «RM-000000-DEMO», «[redteam forms-consent A] test», help-desk
subjects without their accents, a passport whose file was gone. ``clean()`` rewrites them as a finished product would
show them — realistic, FICTIONAL names (the preview's «Valfiorita» and «Collina Verde» are invented places; no name here
is a real organisation's), accented French, references in a plausible format, the sample files present — and says
«fittizio» only where the preview's own strip says it (designpreview.personas.metadata). The e-mail addresses stay in
the reserved ``@example.test`` domain (RFC 2606): they can never belong to anybody.

Idempotent: every change matches the value it replaces, so a second run changes nothing. Refused anywhere but a
preview database (``personas.database_allowed``), whatever the caller says: the command
``manage.py preview_data_clean`` is the only way in, and it runs ``clean(apply=False)`` first unless told ``--apply``.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field

from django.apps import apps
from django.db import transaction

#: The accounts' display names, by e-mail — the nine acceptance accesses and the role accounts their pages name.
DISPLAY_NAMES: dict[str, str] = {
    "qa-doc-person@example.test": "Samira El Amrani",
    "qa-person@example.test": "Hamza Ouazzani",
    "qa-fresh-person@example.test": "Rania Bennis",
    "qa-overdue-person@example.test": "Nadia Benali",
    "qa-waiting-person@example.test": "Youssef Karimi",
    "qa-calm-person@example.test": "Léa Fontaine",
    "qa-company@example.test": "Giulia Ferrante",
    "qa-institution@example.test": "Ufficio Relazioni internazionali — Comune di Valfiorita",
    "qa-university@example.test": "Segreteria didattica — Istituto Collina Verde",
    "demo-acteur-autorise@example.test": "Paolo Ferri",
    "demo-legal-approver@example.test": "Elena Costa",
    "demo-legal-editor@example.test": "Davide Marchetti",
    "demo-operateur@example.test": "Sara Lombardi",
    "demo-professionnel@example.test": "Marco Bellini",
    "seed-actor@example.test": "Alessia Gatti",
    "seed-actor-lapsed@example.test": "Franco Vitale",
    "seed-company@example.test": "Roberto Sala",
    "seed-person@example.test": "Karim Alaoui",
}

#: The person whose file holds the passport was typed «company» and held the person's role (DL54-59): her own
#: dashboard then said «Entreprise» under her name (D-09). She is a person.
ACCOUNT_TYPES: dict[str, str] = {"qa-doc-person@example.test": "person"}

#: What marks a value as a fixture's — removed, the rest of the value kept.
_MARKERS = re.compile(
    r"\s*\((?:données de test|donnée de test(?:, échue)?|prova|organizzazione di prova|entreprise fictive|fictive|"
    r"exemple|compte de test|démonstration|dimostrazione)\)"
)
_DEMO_PREFIX = re.compile(r"^Demo — ")

#: Field rewrites that are not a marker's removal: (model, field, old value, new value).
REWRITES: tuple[tuple[str, str, str, str], ...] = (
    ("companies.CompanyProfile", "registration_number", "RM-000000-DEMO", "RO-187264"),
    ("companies.CompanyProfile", "contact_name", "Référent démonstration", "Giulia Ferrante"),
    ("companies.CompanyProfile", "address_line", "Via della Dimostrazione 1", "Via dell’Industria 12"),
    (
        "companies.NeedAssignment",
        "authorisation_reference",
        "Albo informatico — prot. DEMO/0000/2026",
        "Albo informatico — prot. 0012874/2026",
    ),
    (
        "companies.NeedAssignment",
        "mandate_note",
        "Démonstration : autorisation fictive.",
        "Autorisation enregistrée au dossier de l’entreprise.",
    ),
    ("cases.CaseAssignment", "authorisation_reference", "QA-REVIEW-001", "PRO-2026-0412"),
    (
        "cases.CaseAssignment",
        "mandate_note",
        "Vérification indépendante du parcours d examen (QA).",
        "Vérification indépendante du parcours d’examen.",
    ),
    ("cases.CaseAssignment", "authorisation_reference", "SYNTH-AUT-2026-0148 (donnée de test)", "AUT-2026-0148"),
    ("selection.AuthorizedActor", "authorisation_reference", "SYNTH-AUT-2026-0148 (donnée de test)", "AUT-2026-0148"),
    (
        "selection.AuthorizedActor",
        "authorisation_reference",
        "SYNTH-AUT-2024-0007 (donnée de test, échue)",
        "AUT-2024-0007",
    ),
    (
        "selection.AuthorizedActor",
        "authorisation_register",
        "Registre de test — aucun registre public réel",
        "Registre des autorisations (Vénétie)",
    ),
    (
        "accounts.AccountVerification",
        "evidence_note",
        "Environnement de démonstration — vérification simulée.",
        "Vérification effectuée sur pièces.",
    ),
    (
        "accounts.AccountVerification",
        "evidence_note",
        "Richiesta di prova (anteprima): dati sintetici.",
        "Richiesta di verifica dell’organizzazione.",
    ),
    (
        "accounts.AccountVerification",
        "decision_note",
        "Verifica di prova (anteprima).",
        "Verifica effettuata sui documenti trasmessi.",
    ),
    (
        "portal.Deadline",
        "source_note",
        "Convocation écrite du consulat — donnée synthétique de l’anteprima.",
        "Convocation écrite du consulat.",
    ),
    (
        "portal.Deadline",
        "source_note",
        "Invitation écrite de l’équipe — donnée synthétique de l’anteprima.",
        "Invitation écrite de l’équipe.",
    ),
    ("documents.DocumentRequirement", "title", "Diplome ou titre de formation", "Diplôme ou titre de formation"),
)

#: Fields whose fixture markers («(exemple)», «(prova)», «Demo — » …) are removed wherever they occur.
MARKED_FIELDS: tuple[tuple[str, str], ...] = (
    ("accounts.Organisation", "name"),
    ("accounts.AccountVerification", "declared_organisation"),
    ("academy.TrainingProvider", "name"),
    ("academy.CourseMaterial", "source_title"),
    ("academy.TrainingPlan", "origin_reference"),
    ("academy.SkillGapLine", "source_note"),
    ("portal.Deadline", "title"),
)

#: The Academy's invented providers, by slug — the seed's new names (academy.seeds.PROVIDERS), for rows an earlier
#: seed wrote; and the materials' sources that named them.
PROVIDER_NAMES: dict[str, str] = {
    "centre-langue-exemple": "Centro linguistico Valfiorita",
    "organisme-pro-exemple": "Institut des métiers Oued Lakhdar",
    "universite-partenaire-exemple": "Università Collina Verde",
}
MATERIAL_SOURCES: dict[str, str] = {
    "Centre de langue italienne (exemple)": "Centro linguistico Valfiorita",
    "Organisme de formation (exemple)": "Institut des métiers Oued Lakhdar",
}

#: The help desk: the accents the fixtures dropped, and the duplicates of one request. The census's example ticket
#: (designpreview.live._TICKET) is never touched but for its accents.
ACCENTS: dict[str, str] = {
    "Equivalence de mon diplome pour la voie envisagee": "Équivalence de mon diplôme pour la voie envisagée",
    (
        "Mon diplome a ete obtenu au Maroc en 2019. Je ne sais pas quelle autorite est competente pour en reconnaitre "
        "l'equivalence, ni si cela doit etre fait avant ou apres la constitution du dossier."
    ): (
        "Mon diplôme a été obtenu au Maroc en 2019. Je ne sais pas quelle autorité est compétente pour en reconnaître "
        "l’équivalence, ni si cela doit être fait avant ou après la constitution du dossier."
    ),
    "Justificatif demande par ma checklist": "Justificatif demandé par ma checklist",
    (
        "Je ne sais pas si le justificatif que je detiens correspond a ce que la checklist demande pour ma situation, "
        "ni a quelle date il doit etre produit."
    ): (
        "Je ne sais pas si le justificatif que je détiens correspond à ce que la checklist demande pour ma situation, "
        "ni à quelle date il doit être produit."
    ),
    "Note interne de travail : verifier la date de delivrance avant de repondre.": (
        "Note interne de travail : vérifier la date de délivrance avant de répondre."
    ),
    (
        "Le justificatif que vous detenez correspond a la piece attendue ; il doit etre produit avant la date inscrite "
        "dans votre checklist. Cette reponse est une information juridique et n'est ni une decision ni une garantie de "
        "resultat."
    ): (
        "Le justificatif que vous détenez correspond à la pièce attendue ; il doit être produit avant la date inscrite "
        "dans votre checklist. Cette réponse est une information juridique et n’est ni une décision ni une garantie de "
        "résultat."
    ),
}
#: A second request of the same person, asked three times by a QA pass: the second becomes a request of its own, the
#: third — the same question, answered the same way — leaves.
DISTINCT_TICKET = {
    "subject": "Traduction de mon acte de naissance",
    "question": (
        "Mon acte de naissance est rédigé en arabe. Je ne sais pas si une traduction est demandée pour mon dossier, ni "
        "qui peut la réaliser."
    ),
}

#: The red team's two contact requests (V5.4 red-team pass): the first is the census's example of «une demande»
#: (designpreview.live: ``request-detail``, pk 1), so it is rewritten as an ordinary request; the second leaves.
RED_TEAM_SUBJECT = "[redteam forms-consent A] test"
CONTACT_REQUEST = {
    "name": "Hamza Ouazzani",
    "email": "qa-person@example.test",
    "subject": "Informations sur les parcours de formation avant le départ",
    "message": (
        "Bonjour, je souhaite savoir quelles formations sont proposées avant le départ pour le secteur "
        "agroalimentaire, "
        "et comment elles s’articulent avec mon dossier. Merci."
    ),
}

#: The bytes of the sample file put back where a preview document's file is missing: a one-page PDF that says what it
#: is. Its size and digest are recorded on the row, as an upload would.
SAMPLE_PDF = (
    b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 595 842]/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj\n"
    b"4 0 obj<</Length 66>>stream\nBT /F1 14 Tf 72 770 Td (Italy Legal Entry - document d'exemple) Tj ET\nendstream\n"
    b"endobj\n5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF\n"
)


@dataclass
class Report:
    changes: list[str] = field(default_factory=list)

    def add(self, line: str) -> None:
        self.changes.append(line)


def unmarked(value: str) -> str:
    """``value`` without a fixture's marker: «Comune di Valfiorita (organizzazione di prova)» → «Comune di
    Valfiorita»."""
    return _DEMO_PREFIX.sub("", _MARKERS.sub("", value or "")).strip()


def _model(label: str):
    try:
        return apps.get_model(label)
    except LookupError:
        return None


def _set(row, name: str, value, report: Report, label: str) -> None:
    if getattr(row, name) != value:
        report.add(f"{label}#{row.pk}.{name}")
        setattr(row, name, value)
        row.save(update_fields=[name])


def _accounts(report: Report) -> None:
    User = _model("accounts.User")
    for email, name in DISPLAY_NAMES.items():
        for user in User.objects.filter(email__iexact=email):
            _set(user, "full_name", name, report, "accounts.User")
    for email, kind in ACCOUNT_TYPES.items():
        for user in User.objects.filter(email__iexact=email):
            _set(user, "account_type", kind, report, "accounts.User")


def _rewrites(report: Report) -> None:
    for label, name, old, new in REWRITES:
        model = _model(label)
        if model is None:
            continue
        for row in model.objects.filter(**{name: old}):
            _set(row, name, new, report, label)


def _markers(report: Report) -> None:
    provider = _model("academy.TrainingProvider")
    if provider is not None:  # the seed's own new names first: the marker's removal would only half-name them
        for slug, name in PROVIDER_NAMES.items():
            for row in provider.objects.filter(slug=slug):
                _set(row, "name", name, report, "academy.TrainingProvider")
    for label, name in MARKED_FIELDS:
        model = _model(label)
        if model is None:
            continue
        for row in model.objects.all():
            value = getattr(row, name) or ""
            material = label == "academy.CourseMaterial"
            clean = MATERIAL_SOURCES.get(value, unmarked(value)) if material else unmarked(value)
            if clean and clean != value:
                _set(row, name, clean, report, label)


def _help_desk(report: Report, keep: str) -> None:
    Ticket = _model("helpdesk.HelpdeskTicket")
    Message = _model("helpdesk.TicketMessage")
    if Ticket is None:
        return
    for row in Ticket.objects.all():
        for name in ("subject", "question"):
            value = getattr(row, name)
            if value in ACCENTS:
                _set(row, name, ACCENTS[value], report, "helpdesk.HelpdeskTicket")
    if Message is not None:
        for row in Message.objects.all():
            if row.body in ACCENTS:
                _set(row, "body", ACCENTS[row.body], report, "helpdesk.TicketMessage")
    duplicate = ACCENTS["Justificatif demande par ma checklist"]
    by_person: dict = {}
    for row in Ticket.objects.filter(subject=duplicate).order_by("created_at", "pk"):
        by_person.setdefault(row.person_id, []).append(row)
    for rows in by_person.values():
        if len(rows) < 2:
            continue
        answered = [row for row in rows if row.status == "response_available"]
        # one answered request keeps its words; one other becomes a request of its own; the rest leave
        kept = answered[0] if answered else rows[0]
        others = [row for row in rows if row.pk != kept.pk and str(row.uuid) != keep]
        if others:
            distinct = others[0]
            question = distinct.question
            _set(distinct, "subject", DISTINCT_TICKET["subject"], report, "helpdesk.HelpdeskTicket")
            _set(distinct, "question", DISTINCT_TICKET["question"], report, "helpdesk.HelpdeskTicket")
            if Message is not None:
                for message in Message.objects.filter(ticket=distinct, body=question):
                    _set(message, "body", DISTINCT_TICKET["question"], report, "helpdesk.TicketMessage")
        for row in others[1:]:
            report.add(f"helpdesk.HelpdeskTicket#{row.pk} deleted (a duplicate)")
            row.delete()


def _enquiries(report: Report) -> None:
    Contact = _model("enquiries.ContactRequest")
    if Contact is None:
        return
    rows = list(Contact.objects.filter(subject=RED_TEAM_SUBJECT).order_by("pk"))
    if not rows:
        return
    first, rest = rows[0], rows[1:]
    for name, value in CONTACT_REQUEST.items():
        _set(first, name, value, report, "enquiries.ContactRequest")
    for row in rest:
        report.add(f"enquiries.ContactRequest#{row.pk} deleted (the red team's)")
        row.delete()


def _sample_files(report: Report, *, apply: bool) -> None:
    """Put a sample PDF back wherever a live preview document's file is missing (D-19: a filed passport led to 404).

    The dry run counts the same restorations without writing a file (storage is outside the rolled-back transaction),
    so its count equals the count ``--apply`` then makes.
    """
    Document = _model("documents.PrivateDocument")
    if Document is None:
        return
    from documents.storage import private_storage

    storage = private_storage()
    digest = hashlib.sha256(SAMPLE_PDF).hexdigest()
    for doc in Document.objects.filter(deleted_at__isnull=True, file_removed_at__isnull=True):
        path = f"{doc.owner_id}/{doc.stored_name}"
        if storage.exists(path):
            continue
        if not apply:
            report.add(f"documents.PrivateDocument#{doc.pk} sample file restored")
            continue
        from django.core.files.base import ContentFile

        storage.save(path, ContentFile(SAMPLE_PDF))
        doc.size, doc.sha256 = len(SAMPLE_PDF), digest
        doc.save(update_fields=["size", "sha256"])
        report.add(f"documents.PrivateDocument#{doc.pk} sample file restored")


def clean(*, apply: bool, keep_ticket: str = "") -> Report:
    """
    Every change ``clean`` makes to this database's preview rows — made when ``apply``, reported only otherwise (the
    transaction is rolled back). The caller has checked that the database is a preview's (the command does).
    """
    report = Report()
    with transaction.atomic():
        _accounts(report)
        _rewrites(report)
        _markers(report)
        _help_desk(report, keep_ticket)
        _enquiries(report)
        _sample_files(report, apply=apply)
        if not apply:
            transaction.set_rollback(True)
    return report
