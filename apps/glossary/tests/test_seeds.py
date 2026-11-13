"""Seed tests — the ten prescribed glossary terms are created exactly once, verbatim, and never drift."""

import pytest
from django.core.management import call_command

from cms import locked_content
from cms.models import PublicationStatus
from glossary import registry
from glossary.models import Term
from glossary.seeds import LOCKED_SOURCE_DATETIME, seed_locked_terms

pytestmark = [pytest.mark.django_db, pytest.mark.compliance]


def test_seed_creates_ten_locked_published_terms_with_exact_texts():
    seed_locked_terms()
    prescribed = locked_content.get("p3.glossary.terms", "fr")[0]
    terms = {t.key: t for t in Term.objects.filter(is_locked=True)}
    assert len(terms) == 10
    for entry in prescribed:
        term = terms[entry["key"]]
        assert term.term == entry["term"]
        assert term.definition_fr == entry["definition"]
        assert term.status == PublicationStatus.PUBLISHED
        assert term.last_reviewed_at == LOCKED_SOURCE_DATETIME
        assert term.source
    assert terms["visto_ingresso"].related.filter(key="permesso_di_soggiorno").exists()


def test_seed_is_idempotent_and_does_not_bump_versions():
    seed_locked_terms()
    versions = dict(Term.objects.values_list("key", "version"))
    result = seed_locked_terms()
    assert Term.objects.count() == 10
    assert dict(Term.objects.values_list("key", "version")) == versions
    assert result.startswith("0 locked term(s) created, 0 re-synchronised")


def test_seed_all_command_runs_the_glossary_seed():
    call_command("seed_all", "--only", "glossary", verbosity=0)
    assert Term.objects.filter(is_locked=True).count() == 10
    call_command("seed_all", "--only", "glossary", verbosity=0)
    assert Term.objects.count() == 10


def test_seed_preserves_editorial_fields_but_restores_locked_text():
    seed_locked_terms()
    term = Term.objects.get(key="codice_fiscale")
    term.source = "Source éditoriale"
    term.status = PublicationStatus.DRAFT
    term.related.clear()
    term.save()
    Term.objects.filter(key="codice_fiscale").update(definition_fr="drifted", term="Drifted", is_locked=False)
    seed_locked_terms()
    term.refresh_from_db()
    assert term.source == "Source éditoriale"
    assert term.status == PublicationStatus.DRAFT
    assert term.related.count() == 0, "editorial removal of relations must be respected"
    assert term.is_locked is True
    assert term.term == "Codice fiscale"
    assert term.definition_fr == registry.term("codice_fiscale")["definition"]
