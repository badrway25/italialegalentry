"""
V5.17 §9 — under the production switches (DEBUG False, ``ILE_LEGAL_OPEN_FIELDS_ALLOWED`` False, set on the test
settings; prod.py itself is not loaded here) the privacy page never renders a marker, a highlighted field, «legal
review required» or a configuration question. The publication guard already refuses (``legal.services.publish``);
this file proves the RENDERING path too, in the four languages, on the whole page (not only ``<main>``):

* a row forced to PUBLISHED while its text still carries «[DA COMPLETARE — OF-nn — <class>: …]» renders the pending
  notice only — none of the marker, its id, its class, the highlight, the preview's list of fields;
* the same text with every marker replaced (fictional placeholders, as a verified fact would replace them) renders its
  body, and still none of those traces;
* the switch the preview uses to show them (``ILE_LEGAL_OPEN_FIELDS_ALLOWED``) is False here, as prod.py forces it.
"""

from __future__ import annotations

import re

import pytest
from django.conf import settings

from legal import drafts
from legal.models import OPEN_FIELD_CLASSES, OPEN_FIELD_RE, LegalDocument, LegalKind, LegalStatus
from legal.services import invalidate

pytestmark = [pytest.mark.django_db, pytest.mark.compliance]

LANGS = ("it", "fr", "en", "ar")

#: What production must never render on the privacy page (case-insensitive).
FORBIDDEN = (
    "DA COMPLETARE",
    "legal-open-field",
    "data-open-field",
    "data-open-fields",
    "<mark",
    "campi da completare",
    "data-translation-pending",
    "legal review required",
    "owner confirmation required",
    "production configuration required",
    *(label.lower() for label in OPEN_FIELD_CLASSES),
)
OF_ID = re.compile(r"\bOF-\d+\b")


@pytest.fixture
def privacy(db):
    from legal.services import ensure_documents

    ensure_documents()
    drafts.load_drafts()
    invalidate()
    doc = LegalDocument.objects.get(kind=LegalKind.PRIVACY)
    assert doc.open_fields(), "the draft is expected to carry open fields (V5.16)"
    yield doc
    invalidate()


def _assert_clean(html: str) -> None:
    lowered = html.lower()
    for trace in FORBIDDEN:
        assert trace.lower() not in lowered, trace
    assert not OF_ID.search(html), OF_ID.search(html).group(0)


def test_the_production_switch_is_off_here():
    assert settings.ILE_LEGAL_OPEN_FIELDS_ALLOWED is False
    assert settings.DEBUG is False


@pytest.mark.parametrize("lang", LANGS)
def test_a_published_notice_with_open_fields_renders_no_trace_of_them(client, privacy, lang):
    LegalDocument.objects.filter(pk=privacy.pk).update(status=LegalStatus.PUBLISHED)
    invalidate()
    response = client.get(f"/{lang}/privacy-policy/")
    assert response.status_code == 200
    html = response.content.decode()
    assert 'data-gate="legal-blocked"' in html
    _assert_clean(html)


@pytest.mark.parametrize("lang", LANGS)
def test_a_completed_notice_renders_its_body_and_no_trace_of_the_preview(client, privacy, lang):
    def fill(text: str) -> str:
        return OPEN_FIELD_RE.sub("[valore di prova]", text or "")

    translations = {
        code: {key: fill(value) if isinstance(value, str) else value for key, value in (entry or {}).items()}
        for code, entry in (privacy.translations or {}).items()
    }
    LegalDocument.objects.filter(pk=privacy.pk).update(
        status=LegalStatus.PUBLISHED,
        body_it=fill(privacy.body_it),
        title_it=fill(privacy.title_it),
        translations=translations,
    )
    invalidate()
    doc = LegalDocument.objects.get(pk=privacy.pk)
    assert not doc.open_fields() and doc.is_available
    response = client.get(f"/{lang}/privacy-policy/")
    assert response.status_code == 200
    html = response.content.decode()
    assert 'data-gate="legal-blocked"' not in html
    assert "[valore di prova]" in html  # the body is really rendered
    _assert_clean(html)
