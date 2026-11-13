"""
`seed_all` runs at every deployment (docs/deployment/PRODUCTION_DEPLOYMENT_RUNBOOK.md, step 15). Once a legal source
exists it belongs to the legal referent, who corrects its titles, reference, authority and note in the back-office: a
re-seed must keep those corrections. Until 12 October 2026 `rules.legal_ruleset` wrote every seeded field back with
`update_or_create`, and a corrected citation returned to the build's text at the next release (DevOps review, M9).
"""

from __future__ import annotations

import pytest

from rules import seeds
from rules.models import LegalSource

pytestmark = pytest.mark.django_db


def _spec(key: str) -> dict:
    return next(spec for spec in seeds.SOURCES if spec["key"] == key)


def test_a_new_source_gets_every_seeded_value_and_the_provenance_note():
    seeds.seed()
    for spec in seeds.SOURCES:
        source = LegalSource.objects.get(key=spec["key"])
        assert {name: getattr(source, name) for name in spec} == spec
        assert source.note == seeds.SEED_NOTE


def test_a_reseed_keeps_the_legal_referents_corrections():
    seeds.seed()
    source = LegalSource.objects.get(key="tui-286-1998-art-22")
    corrected = {
        "title_fr": "Travail salarié (intitulé corrigé par le référent)",
        "title_it": "Lavoro subordinato (titolo corretto dal referente)",
        "reference": "D.Lgs. 25 luglio 1998, n. 286, art. 22, comma 2",
        "authority": "Repubblica Italiana — Gazzetta Ufficiale",
        "note": "Verificata alla fonte ufficiale dal referente giuridico.",
        "url": "https://www.normattiva.it/",
    }
    for name, value in corrected.items():
        setattr(source, name, value)
    source.save()

    assert seeds.seed()["sources"] == 0
    source.refresh_from_db()
    assert {name: getattr(source, name) for name in corrected} == corrected


def test_a_reseed_completes_only_what_is_empty():
    seeds.seed()
    LegalSource.objects.filter(key="dpr-394-1999").update(title_it="", authority="")
    seeds.seed()
    source = LegalSource.objects.get(key="dpr-394-1999")
    assert (source.title_it, source.authority) == (
        _spec("dpr-394-1999")["title_it"],
        _spec("dpr-394-1999")["authority"],
    )


def test_the_jurisdiction_follows_the_seed():
    """Not offered by the back-office, and corrected by the seed before: the build keeps it right."""
    seeds.seed()
    LegalSource.objects.filter(key="directive-2016-801").update(jurisdiction="IT")
    seeds.seed()
    assert LegalSource.objects.get(key="directive-2016-801").jurisdiction == "EU"


def test_a_reseed_creates_nothing_twice():
    first = seeds.seed()
    assert first["sources"] == len(seeds.SOURCES)
    assert seeds.seed() == {"sources": 0, "drafted": 0, "legacy_candidates": 0}
