"""Content-lock tests: the prescribed texts must never drift (gate G0)."""

import json
from pathlib import Path

import pytest

from cms import locked_content

CHECKSUM_FILE = Path(__file__).resolve().parents[2] / "apps" / "cms" / "locked_content.sha256.json"

pytestmark = pytest.mark.compliance


def test_checksum_file_matches_registry():
    stored = json.loads(CHECKSUM_FILE.read_text(encoding="utf-8"))
    for lang, table in locked_content.LOCKED_TEXTS.items():
        assert lang in stored, f"missing checksum table for {lang}; run scripts/lock_content.py after review"
        current = locked_content.checksums(lang)
        assert current == stored[lang], (
            "Locked content changed. If this is an official update, regenerate checksums with "
            "scripts/lock_content.py and record the source in docs/CONTENT_SOURCE_MAP.md"
        )


def test_registry_keys_are_stable():
    expected_prefixes = ("p1.", "p2.", "p3.", "legal.")
    for key in locked_content.keys():
        assert key.startswith(expected_prefixes), key


@pytest.mark.parametrize(
    "key, expected",
    [
        ("p1.companies.title", "DE QUELS PROFILS PROFESSIONNELS VOTRE ENTREPRISE A-T-ELLE BESOIN ?"),
        ("p1.companies.form.button", "MANIFESTEZ VOTRE INTÉRÊT POUR LE PROJET"),
        ("p1.trademark.mark", "Italy Legal Entry™"),
        ("p1.email.public_contact", "contact@agamieuromed.org"),
        ("p2.forum.header.meta", "Rovigo — 2 octobre 2026 — Sala della Gran Guardia — 15h00–18h00"),
        ("p2.forum.registration.button_primary", "PARTICIPEZ AU FORUM"),
        ("p2.home.banner.button", "DÉCOUVREZ LE FORUM"),
        ("p3.hero.subtitle", "Le parcours régulier vers l’Italie, de l’orientation à l’intégration."),
        ("p3.reserved.button", "CONNEXION"),
    ],
)
def test_exact_prescribed_strings(key, expected):
    assert locked_content.text(key, "fr") == expected


def test_company_form_field_order_is_prescribed():
    fields = locked_content.get("p1.companies.form.fields", "fr")[0]
    assert fields[0] == "Raison sociale de l’entreprise"
    assert fields[3] == "Nom et fonction du référent"
    assert fields[-1] == "Notes (champ libre)"
    assert len(fields) == 14


def test_forum_categories_are_prescribed():
    cats = locked_content.get("p2.forum.registration.categories", "fr")[0]
    assert cats == [
        "Institution",
        "Entreprise",
        "Association professionnelle / Chambre de Commerce",
        "Université / Organisme de formation",
        "Professionnel",
        "Organisme du travail",
        "Représentation diplomatique ou consulaire",
        "Autre",
    ]


def test_fallback_to_french_for_other_languages():
    value, lang = locked_content.get("p3.antifraud.title", "ar")
    assert lang == "fr"
    assert value == "ATTENTION AUX FRAUDES"


def test_no_registered_mark_in_locked_content():
    for key, value in locked_content.LOCKED_TEXTS["fr"].items():
        assert "®" not in locked_content.canonical(value), key


def test_cookie_policy_internal_note_is_not_in_registry():
    dump = locked_content.canonical(locked_content.LOCKED_TEXTS["fr"]["legal.cookies.fr_courtesy"])
    assert "Note opérationnelle" not in dump
    assert "Google Analytics" not in dump
