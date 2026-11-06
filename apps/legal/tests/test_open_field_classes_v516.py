"""
V5.16 (28 Oct 2026) — the privacy notice's open fields are classified, not removed.

What this file pins:

* every «[DA COMPLETARE …]» marker in A, in every language, names exactly one class — PRODUCTION CONFIGURATION
  REQUIRED, OWNER CONFIRMATION REQUIRED or LEGAL REVIEW REQUIRED — and the same class for the same OF id everywhere;
* the classes are the directive's: the infrastructure facts (§1, §10) are production configuration, the controller
  (§2, OF-01) is the owner's confirmation with AGAMI APS as the candidate (Italy Legal Entry is not
  substituted as controller unless the owner confirms it is a separate legal entity), the
  bases, art. 9, roles, DPO status and retention policies (§4, §5, §7, §9, §11) are the legal review;
* DigitalOcean is named as the intended hosting provider only — no region, DPA state or transfer is stated;
* production still refuses to publish a text that carries a marker of ANY class; the preview shows the class.
"""

from __future__ import annotations

import re

import pytest
from django.core.exceptions import ValidationError

from legal import drafts
from legal.models import (
    OPEN_FIELD_CLASS_RE,
    OPEN_FIELD_CLASSES,
    OPEN_FIELD_ID_RE,
    OPEN_FIELD_RE,
    TRANSLATION_LANGUAGES,
    LegalDocument,
    LegalKind,
    LegalStatus,
    open_field_class,
)
from legal.services import invalidate, publish

LANGS = ("it", *TRANSLATION_LANGUAGES)
PC, OC, LR = "PRODUCTION CONFIGURATION REQUIRED", "OWNER CONFIRMATION REQUIRED", "LEGAL REVIEW REQUIRED"
#: V5.16's assignment, OF id → class (OF-09 and OF-11 are not in the text: the forms are closed).
EXPECTED = {
    "OF-01": OC,  # §2: the controller — AGAMI APS as candidate, the owner confirms
    "OF-02": PC,  # §1, §10: DigitalOcean region, DB/storage region, DPA acceptance, transfers as configured
    "OF-03": PC,  # §1: SMTP provider actually used, mailbox hosting
    "OF-04": PC,  # §1: off-server backups, backup retention
    "OF-05": PC,  # §1, §12: nginx rotation, journald retention on the real server
    "OF-06": LR,  # §11: security audit trail retention policy
    "OF-07": LR,  # §11: retention policies (accounts, documents, cases, outbox)
    "OF-08": LR,  # §7: DPO STATUS = TO BE CONFIRMED
    "OF-10": LR,  # §4: the legal basis of the reserved area
    "OF-12": LR,  # §9: recipient roles
    "OF-13": LR,  # §5: SPECIAL CATEGORY LEGAL BASIS REQUIRED
}


def _markers(lang: str) -> list[str]:
    return OPEN_FIELD_RE.findall(drafts.read(LegalKind.PRIVACY, lang)["body"])


@pytest.mark.parametrize("lang", LANGS)
def test_every_marker_names_exactly_one_class_and_the_directives_one(lang):
    markers = _markers(lang)
    assert markers
    for marker in markers:
        assert len(OPEN_FIELD_CLASS_RE.findall(marker)) == 1, marker
        ids = OPEN_FIELD_ID_RE.findall(marker)
        # the marker's own id is the first one (a marker may cite another, «… (OF-03)»)
        assert open_field_class(marker) == EXPECTED[ids[0]], marker
    assert {OPEN_FIELD_ID_RE.findall(m)[0] for m in markers} == set(EXPECTED), lang


def test_the_classes_are_the_same_in_every_language():
    def classes(lang):
        return sorted((OPEN_FIELD_ID_RE.findall(m)[0], open_field_class(m)) for m in _markers(lang))

    master = classes("it")
    for lang in TRANSLATION_LANGUAGES:
        assert classes(lang) == master, lang


@pytest.mark.parametrize("lang", LANGS)
def test_the_controller_is_agami_aps_as_a_candidate_to_confirm_not_italy_legal_entry_by_substitution(lang):
    body = drafts.read(LegalKind.PRIVACY, lang)["body"]
    of01 = [m for m in _markers(lang) if OPEN_FIELD_ID_RE.findall(m)[0] == "OF-01"]
    assert len(of01) == 1 and OC in of01[0] and "AGAMI APS" in of01[0]
    for wrong in (
        "titolare del trattamento è Italy Legal Entry",
        "responsable du traitement est Italy Legal Entry",
        "controller is Italy Legal Entry",
    ):
        assert wrong not in body


@pytest.mark.parametrize("lang", LANGS)
def test_digitalocean_is_only_the_intended_provider_no_infrastructure_fact_is_stated(lang):
    body = drafts.read(LegalKind.PRIVACY, lang)["body"]
    prose = OPEN_FIELD_RE.sub("", body)
    assert prose.count("DigitalOcean") == 1, "named once, as the intended hosting provider, outside the markers"
    for marker in _markers(lang):
        if "DigitalOcean" in marker:
            assert PC in marker
    for invented in ("FRA1", "AMS3", "LON1", "Frankfurt", "Francoforte", "Amsterdam", "Londra", "London"):
        assert invented not in body, invented


@pytest.mark.parametrize("label", list(OPEN_FIELD_CLASSES))
def test_production_refuses_a_marker_of_every_class(db, superuser, label):
    from legal.services import ensure_documents

    ensure_documents()
    doc = LegalDocument.objects.get(kind=LegalKind.COOKIES)
    doc.title_it = "Prova"
    doc.body_it = f"## 1. Prova\n\nTesto.\n\n[DA COMPLETARE — OF-99 — {label}: prova]\n"
    doc.translations = {}
    doc.source_reference = "test"
    doc.status = LegalStatus.DRAFT
    doc.save()
    with pytest.raises(ValidationError) as exc:
        publish(doc, superuser)
    assert label in str(exc.value) and "OF-99" in str(exc.value)
    doc.refresh_from_db()
    assert doc.status == LegalStatus.DRAFT


def test_the_preview_lists_the_open_fields_by_class(client, db, superuser, settings):
    from legal.services import ensure_documents

    settings.ILE_LEGAL_OPEN_FIELDS_ALLOWED = True
    ensure_documents()
    drafts.load_drafts()
    invalidate()
    publish(LegalDocument.objects.get(kind=LegalKind.PRIVACY), superuser)
    invalidate()
    try:
        html = client.get("/it/privacy-policy/").content.decode()
        lines = re.findall(r"<li data-open-field-class-list>([^<]*)</li>", html)
        assert [line.split(":")[0] for line in lines] == [PC, OC, LR]
        assert "OF-01" in lines[1] and "OF-02" in lines[0] and "OF-13" in lines[2]
        for slug in OPEN_FIELD_CLASSES.values():
            assert f'data-open-field-class="{slug}"' in html
        assert 'data-open-field-class="unclassified"' not in html
    finally:
        settings.ILE_LEGAL_OPEN_FIELDS_ALLOWED = False
        invalidate()
