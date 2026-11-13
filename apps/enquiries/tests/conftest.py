"""Fixtures and helpers shared by the enquiries test-suite."""

from __future__ import annotations

import time

import pytest
from django.core.management import call_command
from django.test import RequestFactory

from consents.services import record_consent
from enquiries.models import CollaborationProposal, CompanyNeedsRequest, ContactRequest, ProposalKind

# Shared project fixtures (tests/conftest.py is not an ancestor of this directory, so re-export them).
from tests.conftest import (  # noqa: F401
    _clear_caches,
    before_phase3,
    client_ar,
    client_fr,
    legal_published,
    person_user,
    phase3_open,
    set_flag,
    staff_user,
    superuser,
    url,
    user_factory,
)


@pytest.fixture
def seeded(db):
    """
    Foundation seeds this app depends on (roles/permissions, legal documents, consent texts).
    Deliberately narrower than the project-wide ``seeded`` so that a sibling app in the middle of
    its own migration work cannot block this suite; the global crawl in tests/compliance still
    exercises the enquiries routes with every seed.
    """
    from core import flags
    from legal.services import invalidate as legal_invalidate

    for prefix in ("accounts.", "legal.", "consents."):
        call_command("seed_all", "--only", prefix, verbosity=0)
    flags.invalidate()
    legal_invalidate()


COMPANY_URL = "/fr/entreprises/recueil-des-besoins/"
INSTITUTION_URL = "/fr/collaboration/institutions/"
UNIVERSITY_URL = "/fr/collaboration/universites-formation/"
CONTACT_URL = "/fr/contact/formulaire/"
DONE_URL = "/fr/demande-transmise/"
INBOX = "contact@agamieuromed.org"


def honeypot(payload: dict, *, started_seconds_ago: int = 30, website_url: str = "") -> dict:
    """Add the anti-spam fields a real browser would submit (empty honeypot, plausible fill time)."""
    return {**payload, "website_url": website_url, "form_started_at": str(int(time.time()) - started_seconds_ago)}


def company_payload(**overrides) -> dict:
    data = {
        "company_name": "Officine Meccaniche Rossi S.r.l.",
        "sector": "Métallurgie",
        "headquarters": "Rovigo (RO)",
        "contact_name_and_role": "Maria Rossi — Responsable RH",
        "email": "Maria.Rossi@example.test",
        "phone": "+39 0425 000000",
        "profiles_needed": "Soudeurs, opérateurs CNC",
        "indicative_headcount": "5 à 10",
        "qualifications_required": "Diplôme technique",
        "experience_required": "2 ans",
        "language_requirements": "Italien A2",
        "training_needs": "Sécurité au travail",
        "indicative_timeline": "Premier semestre 2027",
        "notes": "",
        "consent": "on",
    }
    data.update(overrides)
    return data


def collaboration_payload(**overrides) -> dict:
    data = {
        "organisation_name": "Université de Casablanca",
        "organisation_type": "Université",
        "contact_name_and_role": "Ahmed Alami — Vice-recteur",
        "email": "a.alami@example.test",
        "phone": "",
        "country": "Maroc",
        "proposal": "Programme conjoint de formation avant le départ.",
        "consent": "on",
    }
    data.update(overrides)
    return data


def contact_payload(**overrides) -> dict:
    data = {
        "name": "Jean Dupont",
        "email": "jean.dupont@example.test",
        "subject": "Question sur le projet",
        "message": "Bonjour, je souhaite en savoir plus.",
        "consent": "on",
    }
    data.update(overrides)
    return data


@pytest.fixture
def rf_request():
    request = RequestFactory().get("/fr/")
    request.user = None
    return request


@pytest.fixture
def make_company(db):
    def _make(email="company@example.test", owner=None, **fields):
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
def make_proposal(db):
    def _make(email="inst@example.test", owner=None, kind=ProposalKind.INSTITUTION, **fields):
        purpose = "university_proposal" if kind == ProposalKind.UNIVERSITY else "institution_proposal"
        consent = record_consent(None, purpose, email=email, user=owner, language="fr")
        defaults = {
            "organisation_name": "Regione X",
            "contact_name_and_role": "Referente",
            "country": "Italie",
            "proposal": "Coopération institutionnelle.",
        }
        defaults.update(fields)
        obj = CollaborationProposal(email=email, consent=consent, owner=owner, kind=kind, language="fr", **defaults)
        obj.duplicate_hash = obj.compute_duplicate_hash()
        obj.save()
        return obj

    return _make


@pytest.fixture
def make_contact(db):
    def _make(email="someone@example.test", owner=None, **fields):
        consent = record_consent(None, "contact", email=email, user=owner, language="fr")
        defaults = {"name": "Someone", "subject": "Hello", "message": "Message"}
        defaults.update(fields)
        obj = ContactRequest(email=email, consent=consent, owner=owner, language="fr", **defaults)
        obj.duplicate_hash = obj.compute_duplicate_hash()
        obj.save()
        return obj

    return _make
