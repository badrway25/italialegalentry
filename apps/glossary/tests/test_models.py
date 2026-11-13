"""Unit tests — glossary models and services (no HTTP)."""

import datetime as dt

import pytest
from django.core.exceptions import ValidationError

from cms.models import PublicationStatus, TranslationStatus
from glossary import registry, services
from glossary.models import Term, TermTranslation, initial_letter

pytestmark = pytest.mark.django_db


def test_registry_exposes_ten_prescribed_terms_in_order():
    keys = registry.keys()
    assert len(keys) == 10
    assert keys[0] == "visto_ingresso" and keys[-1] == "codice_fiscale"
    assert registry.term("codice_fiscale")["term"] == "Codice fiscale"
    assert registry.term("unknown") is None


@pytest.mark.parametrize(
    "text, expected",
    [("Visto d’ingresso", "V"), ("Émigration", "E"), (" questura", "Q"), ("", "0-9"), ("123", "0-9"), ("730", "0-9")],
)
def test_initial_letter_strips_accents_and_uppercases(text, expected):
    assert initial_letter(text) == expected


def test_locked_term_save_re_asserts_registry_text():
    term = Term.objects.create(key="codice_fiscale", is_locked=True, term="tampered", definition_fr="tampered")
    term.refresh_from_db()
    assert term.term == "Codice fiscale"
    assert term.definition_fr == registry.term("codice_fiscale")["definition"]
    term.definition_fr = "tampered again"
    term.save()
    term.refresh_from_db()
    assert term.definition_fr == registry.term("codice_fiscale")["definition"]


def test_unlocked_term_keeps_editorial_text():
    term = Term.objects.create(key="isee", term="ISEE", definition_fr="indicateur de la situation économique.")
    term.refresh_from_db()
    assert term.is_locked is False and term.term == "ISEE"
    assert term.get_absolute_url() == "/fr/glossaire/isee/"


def test_clean_rejects_locking_a_key_outside_the_registry():
    term = Term(key="not_in_registry", is_locked=True, term="x", definition_fr="y")
    with pytest.raises(ValidationError) as exc:
        term.full_clean()
    assert "is_locked" in exc.value.message_dict


def test_translation_rules():
    term = Term.objects.create(key="codice_fiscale", is_locked=True, term="", definition_fr="")
    with pytest.raises(ValidationError):
        TermTranslation(master=term, language="fr", definition="x").full_clean()
    row = TermTranslation(master=term, language="it", definition="x", status=TranslationStatus.PUBLISHED)
    with pytest.raises(ValidationError) as exc:
        row.full_clean()
    assert "source" in exc.value.message_dict
    row.source = "testo ufficiale"
    row.full_clean()


def test_related_terms_are_symmetrical():
    a = Term.objects.create(key="visto_ingresso", is_locked=True, term="", definition_fr="", status="published")
    b = Term.objects.create(key="nulla_osta", is_locked=True, term="", definition_fr="", status="published")
    a.related.add(b)
    assert list(b.related.all()) == [a]


def test_live_terms_and_letter_groups():
    Term.objects.create(key="visto_ingresso", is_locked=True, term="", definition_fr="", status="published")
    Term.objects.create(key="codice_fiscale", is_locked=True, term="", definition_fr="", status="published")
    Term.objects.create(key="carta_blu_ue", is_locked=True, term="", definition_fr="", status="published")
    Term.objects.create(key="draft", term="Zeta", definition_fr="z")  # draft, never listed
    Term.objects.create(
        key="expired",
        term="Alfa",
        definition_fr="a",
        status=PublicationStatus.PUBLISHED,
        unpublish_at=dt.datetime(2020, 1, 1, tzinfo=dt.UTC),
    )
    entries = services.entries_for(services.live_terms(), "fr")
    groups = services.letter_groups(entries)
    assert [g.letter for g in groups] == ["C", "V"]
    assert [e.term for e in groups[0].entries] == ["Carta blu UE", "Codice fiscale"]


def test_entry_for_uses_registry_and_published_translation_only():
    term = Term.objects.create(key="codice_fiscale", is_locked=True, term="", definition_fr="", status="published")
    Term.objects.filter(pk=term.pk).update(definition_fr="db mirror tampered")
    term.refresh_from_db()
    entry = services.entry_for(term, "fr")
    assert entry.definition == registry.term("codice_fiscale")["definition"]
    assert entry.is_fallback is False and entry.term_lang == "it"
    entry_en = services.entry_for(term, "en")
    assert entry_en.is_fallback is True and entry_en.lang == "fr"
    TermTranslation.objects.create(master=term, language="en", definition="Italian tax code.", status="draft")
    term = Term.objects.prefetch_related("translations").get(pk=term.pk)
    assert services.entry_for(term, "en").is_fallback is True
    TermTranslation.objects.filter(master=term).update(status=TranslationStatus.PUBLISHED, source="official")
    term = Term.objects.prefetch_related("translations").get(pk=term.pk)
    entry_en = services.entry_for(term, "en")
    assert entry_en.is_fallback is False and entry_en.definition == "Italian tax code."
    assert entry_en.term == "Codice fiscale" and entry_en.term_lang == "it"


def test_search_matches_term_definition_and_key():
    Term.objects.create(key="codice_fiscale", is_locked=True, term="", definition_fr="", status="published")
    Term.objects.create(key="nulla_osta", is_locked=True, term="", definition_fr="", status="published")
    assert [t.key for t in services.search_terms("fiscale")] == ["codice_fiscale"]
    assert [t.key for t in services.search_terms("Sportello Unico")] == ["nulla_osta"]
    assert [t.key for t in services.search_terms("nulla osta")] == ["nulla_osta"]
    assert list(services.search_terms("zzzz-nothing")) == []


def test_jsonld_defined_term_set_only_live(rf):
    live = Term.objects.create(key="codice_fiscale", is_locked=True, term="", definition_fr="", status="published")
    draft = Term.objects.create(key="draft", term="Zeta", definition_fr="z")
    request = rf.get("/fr/glossaire/")
    data = services.term_set_jsonld(services.entries_for([live, draft], "fr"), "fr", request)
    assert data["@type"] == "DefinedTermSet"
    assert [t["name"] for t in data["hasDefinedTerm"]] == ["Codice fiscale"]
    assert data["hasDefinedTerm"][0]["url"].endswith("/fr/glossaire/codice_fiscale/")
    single = services.term_jsonld(services.entry_for(live, "fr"), request, "http://testserver/fr/glossaire/")
    assert single["@type"] == "DefinedTerm" and single["inDefinedTermSet"].endswith("/fr/glossaire/")
    assert set(single) == {"@context", "@type", "name", "description", "inLanguage", "url", "inDefinedTermSet"}


def test_link_map_is_cached_and_invalidated_on_save(set_flag):
    term = Term.objects.create(key="codice_fiscale", is_locked=True, term="", definition_fr="", status="published")
    assert "codice_fiscale" in services.link_map()
    term.status = PublicationStatus.DRAFT
    term.save()
    assert "codice_fiscale" not in services.link_map()
    assert services.link_target("codice_fiscale") is None  # gate closed
