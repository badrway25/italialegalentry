# ruff: noqa: F811 — pytest fixtures legitimately shadow the imported shared fixture names
"""Fixtures of the reserved-area test-suite: two fully separated accounts (A / B) with real rows."""

from __future__ import annotations

import datetime as dt

import pytest
from django.core.management import call_command

from accounts import roles
from accounts.models import AccountType, Membership, MembershipRole, Organisation, OrganisationKind
from consents.services import record_consent
from core import clock
from documents.models import DocumentKind, PrivateDocument, ScanStatus
from enquiries.models import CollaborationProposal, CompanyNeedsRequest, ContactRequest, ProposalKind
from portal.models import Deadline, DeadlineKind, Message

# Shared project fixtures (tests/conftest.py is not an ancestor of this directory, so re-export them).
from tests.conftest import (  # noqa: F401
    _clear_caches,
    after_midnight_in_rome,
    before_phase3,
    legal_published,
    person_user,
    phase3_open,
    set_flag,
    staff_user,
    superuser,
    url,
    user_factory,
)

DASHBOARD = "/fr/espace-reserve/"
REQUESTS = "/fr/espace-reserve/mes-demandes/"
PATHWAYS = "/fr/espace-reserve/mon-parcours/"
DOCUMENTS = "/fr/espace-reserve/mes-documents/"
SITUATION = "/fr/espace-reserve/ma-situation/"
DEADLINES = "/fr/espace-reserve/mes-echeances/"
MESSAGES = "/fr/espace-reserve/communications/"
LOGIN = "/fr/compte/login/"


@pytest.fixture
def seeded(db):
    """
    Foundation seeds the portal depends on (roles, legal documents, consent texts, orientation rule
    set). Narrower than the project-wide ``seeded`` so a sibling app in the middle of its own work
    cannot block this suite.
    """
    from core import flags
    from legal.services import invalidate as legal_invalidate

    for prefix in ("accounts.", "legal.", "consents.", "orientation.", "portal."):
        call_command("seed_all", "--only", prefix, verbosity=0)
    flags.invalidate()
    legal_invalidate()


@pytest.fixture(autouse=True)
def _private_root(settings, tmp_path):
    settings.PRIVATE_MEDIA_ROOT = tmp_path / "private"
    settings.MEDIA_ROOT = tmp_path / "media"
    yield


@pytest.fixture
def alice(user_factory):
    return user_factory(
        "alice.alpha@example.test",
        role=roles.PERSON,
        full_name="Alice ALPHA-UNIQUE",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )


@pytest.fixture
def bob(user_factory):
    return user_factory(
        "bob.bravo@example.test",
        role=roles.PERSON,
        full_name="Bob BRAVO-UNIQUE",
        account_type=AccountType.PERSON,
        terms_accepted_at=clock.now(),
    )


@pytest.fixture
def make_company_request(db):
    def _make(owner, email=None, **fields):
        email = email or owner.email
        consent = record_consent(None, "company_needs", email=email, user=owner, language="fr")
        defaults = {
            "company_name": "ACME S.p.A.",
            "sector": "Industrie",
            "headquarters": "Padova (PD)",
            "contact_name_and_role": "Luca Bianchi — HR",
            "phone": "+39 049 0000000",
            "profiles_needed": "Techniciens de maintenance",
        }
        defaults.update(fields)
        obj = CompanyNeedsRequest(email=email, consent=consent, owner=owner, language="fr", **defaults)
        obj.duplicate_hash = obj.compute_duplicate_hash()
        obj.save()
        return obj

    return _make


@pytest.fixture
def make_contact_request(db):
    def _make(owner, email=None, **fields):
        email = email or owner.email
        consent = record_consent(None, "contact", email=email, user=owner, language="fr")
        defaults = {"name": owner.full_name or "Nom", "subject": "Question", "message": "Bonjour."}
        defaults.update(fields)
        obj = ContactRequest(email=email, consent=consent, owner=owner, language="fr", **defaults)
        obj.duplicate_hash = obj.compute_duplicate_hash()
        obj.save()
        return obj

    return _make


@pytest.fixture
def make_proposal(db):
    def _make(owner, email=None, **fields):
        email = email or owner.email
        consent = record_consent(None, "institution_proposal", email=email, user=owner, language="fr")
        defaults = {
            "kind": ProposalKind.INSTITUTION,
            "organisation_name": "Organisme X",
            "contact_name_and_role": "Référent",
            "country": "Italie",
            "proposal": "Coopération.",
        }
        defaults.update(fields)
        obj = CollaborationProposal(email=email, consent=consent, owner=owner, language="fr", **defaults)
        obj.duplicate_hash = obj.compute_duplicate_hash()
        obj.save()
        return obj

    return _make


@pytest.fixture
def make_document(db):
    counter = {"n": 0}

    def _make(owner, name="piece.pdf", organisation=None, scan_status=ScanStatus.CLEAN, **fields):
        counter["n"] += 1
        return PrivateDocument.objects.create(
            owner=owner,
            organisation=organisation,
            kind=fields.pop("kind", DocumentKind.OTHER),
            original_name=name,
            stored_name=f"stored-{counter['n']:04d}-{owner.pk}.pdf",
            content_type="application/pdf",
            size=1234,
            sha256=f"{counter['n']:064d}",
            scan_status=scan_status,
            **fields,
        )

    return _make


@pytest.fixture
def make_message(db, staff_user):
    def _make(recipient, subject="Information", body="Bonjour.", **fields):
        return Message.objects.create(recipient=recipient, sender=staff_user, subject=subject, body=body, **fields)

    return _make


@pytest.fixture
def make_deadline(db):
    def _make(owner, title="Dépôt du dossier", days=10, **fields):
        fields.setdefault("kind", DeadlineKind.DOCUMENT)
        return Deadline.objects.create(
            owner=owner, title=title, due_on=clock.today() + dt.timedelta(days=days), **fields
        )

    return _make


@pytest.fixture
def make_organisation(db):
    def _make(name, user=None, role=MembershipRole.OWNER, kind=OrganisationKind.COMPANY, **fields):
        organisation = Organisation.objects.create(name=name, kind=kind, **fields)
        if user is not None:
            Membership.objects.create(user=user, organisation=organisation, role=role)
        return organisation

    return _make


@pytest.fixture
def company_a(user_factory, make_organisation):
    user = user_factory(
        "rh@alpha-industrie.example.test",
        role=roles.COMPANY,
        full_name="Resp ALPHA-INDUSTRIE",
        account_type=AccountType.COMPANY,
        terms_accepted_at=clock.now(),
    )
    organisation = make_organisation("ALPHA-INDUSTRIE S.r.l.", user, city="Rovigo", country="Italie")
    return user, organisation


@pytest.fixture
def company_b(user_factory, make_organisation):
    user = user_factory(
        "rh@bravo-logistica.example.test",
        role=roles.COMPANY,
        full_name="Resp BRAVO-LOGISTICA",
        account_type=AccountType.COMPANY,
        terms_accepted_at=clock.now(),
    )
    organisation = make_organisation("BRAVO-LOGISTICA S.p.A.", user, city="Padova", country="Italie")
    return user, organisation


@pytest.fixture
def completed_orientation(db, seeded):
    """A completed orientation session (real active rule set) attached to the given account."""
    from orientation.models import OrientationResult, OrientationSession, Outcome, SessionStatus
    from orientation.services import active_ruleset

    def _make(user):
        ruleset = active_ruleset()
        assert ruleset is not None, "orientation seed must provide an active ruleset"
        outcome = Outcome.objects.filter(ruleset=ruleset).order_by("id").first()
        session = OrientationSession.objects.create(ruleset=ruleset, user=user, status=SessionStatus.COMPLETED)
        result = OrientationResult.objects.create(
            session=session, outcome=outcome, ruleset_version=ruleset.version, result_text_fr=outcome.explanation_fr
        )
        return session, result

    return _make
