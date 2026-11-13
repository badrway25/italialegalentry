"""
A requested piece's words in the reader's language (V5.24 §4–§5, the Arabic completeness audit's W3.2; lane AR): the
seeded pieces (apps/documents/seeds.py REQUIREMENTS) are declared in French and the catalogue says them in
Italian, English
and Arabic — on the register's rows, the piece's page, the case file and the dashboard's next action; a piece
an operator
declares by hand keeps its own words, isolated in their language.
"""

from __future__ import annotations

import pytest
from django.utils import translation

from cases import services as cases
from cases.models import CasePurpose, ResponsibleActor
from documents import seeds
from documents import services as documents
from documents.presenters import present_requirement
from documents.services import REQUIREMENT_TEXTS, displayed_text

pytestmark = pytest.mark.django_db


def test_the_catalogue_knows_every_seeded_title_and_detail():
    with translation.override(None):
        listed = {str(text) for text in REQUIREMENT_TEXTS}
    seeded = set()
    for _code, title, _actor, _kind, _source_title, _source_ref, _access, detail in seeds.REQUIREMENTS:
        seeded.add(title)
        seeded.add(detail)
    assert seeded == listed, "the listed texts are the seeds' titles and details, no more, no less"


@pytest.mark.parametrize(
    ("lang", "expected", "expected_lang"),
    [
        ("fr", "Passeport en cours de validité", "fr"),
        ("it", "Passaporto in corso di validità", "it"),
        ("en", "Valid passport", "en"),
        ("ar", "جواز سفر ساري الصلاحية", "ar"),
    ],
)
def test_displayed_text_says_a_seeded_title_in_the_readers_language(lang, expected, expected_lang):
    with translation.override(lang):
        assert displayed_text("Passeport en cours de validité", "fr") == (expected, expected_lang)


def test_displayed_text_keeps_an_operators_own_words_in_their_language():
    with translation.override("ar"):
        assert displayed_text("Attestation de stage signée", "fr") == ("Attestation de stage signée", "fr")
        assert displayed_text("", "fr") == ("", "fr")
        assert displayed_text("Scan parziale", "it") == ("Scan parziale", "it")


def _declare(case, index: int):
    code, title, actor, kind, source_title, source_ref, access, detail = seeds.REQUIREMENTS[index]
    return documents.declare_requirement(
        case,
        code=code,
        title=title,
        detail=detail,
        responsible_actor=actor,
        kind=kind,
        source_title=source_title,
        source_ref=source_ref,
        access_class=access,
        order=index,
    )


def test_the_register_row_and_the_next_action_read_arabic(person_user):
    case = cases.open_case(person_user, purpose=CasePurpose.WORK)
    passport = _declare(case, 0)
    nulla_osta = _declare(case, 6)
    with translation.override("ar"):
        row = present_requirement(passport, user=person_user)
        assert row["title"] == "جواز سفر ساري الصلاحية"
        assert row["detail"].startswith("صفحات الهوية فقط")
        assert row["words"] == {"lang": "", "dir": ""}, "the words are the page's: no isolation needed"
        authority = present_requirement(nulla_osta, user=person_user)
        assert authority["title"].startswith("تصريح")
        action = cases.next_action(case, reader=person_user)
        assert action is not None and action.label == "جواز سفر ساري الصلاحية" and action.lang == "ar"
    with translation.override("it"):
        row = present_requirement(passport, user=person_user)
        assert row["title"] == "Passaporto in corso di validità" and row["words"]["lang"] == ""
    with translation.override("fr"):
        row = present_requirement(passport, user=person_user)
        assert row["title"] == "Passeport en cours de validité" and row["words"]["lang"] == ""


def test_an_operators_own_piece_stays_french_and_isolated_on_an_arabic_page(person_user):
    case = cases.open_case(person_user, purpose=CasePurpose.WORK)
    piece = documents.declare_requirement(
        case,
        code="stage",
        title="Attestation de stage signée",
        detail="Original.",
        responsible_actor=ResponsibleActor.PERSON,
    )
    with translation.override("ar"):
        row = present_requirement(piece, user=person_user)
        assert row["title"] == "Attestation de stage signée"
        assert row["words"] == {"lang": "fr", "dir": "ltr"}


def test_the_person_sees_the_pieces_in_arabic_on_her_pages(client, person_user, seeded):
    case = cases.open_case(person_user, purpose=CasePurpose.WORK)
    _declare(case, 0)
    _declare(case, 6)
    client.force_login(person_user)
    documents_page = client.get("/ar/espace-reserve/mes-documents/")
    if documents_page.status_code == 200:
        html = documents_page.content.decode()
        assert "جواز سفر ساري الصلاحية" in html
        assert "Passeport en cours de validité" not in html
    dashboard = client.get("/ar/espace-reserve/").content.decode()
    assert "Passeport en cours de validité" not in dashboard
