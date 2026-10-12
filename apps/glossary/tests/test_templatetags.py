"""Tests for {% glossary_link %} — contextual links usable from other apps' content."""

import pytest
from django.template import Context, Template
from django.utils import translation

from cms.models import PublicationStatus
from glossary.models import Term
from glossary.seeds import seed_locked_terms

pytestmark = pytest.mark.django_db


def _render(source: str, lang: str = "fr", **context) -> str:
    with translation.override(lang):
        return Template("{% load glossary_links %}" + source).render(Context(context))


@pytest.fixture
def glossary_seeded(db):
    seed_locked_terms()


def test_renders_inline_link_with_italian_term_when_gate_open(glossary_seeded, phase3_open):
    html = _render('{% glossary_link "codice_fiscale" %}')
    assert html.startswith('<a class="glossary-link" href="/fr/glossaire/codice_fiscale/"')
    assert 'data-glossary-key="codice_fiscale"' in html
    assert 'lang="it">Codice fiscale</a>' in html
    assert 'title="identifiant fiscal italien' in html


def test_custom_label_has_no_lang_attribute_and_variables_are_escaped(glossary_seeded, phase3_open):
    html = _render('{% glossary_link "codice_fiscale" "code fiscal" %}')
    assert ">code fiscal</a>" in html
    assert 'lang="it"' not in html
    # A label coming from a context variable (e.g. CMS data) is escaped; template literals are trusted.
    html = _render('{% glossary_link "codice_fiscale" label %}', label="code fiscal <b>")
    assert ">code fiscal &lt;b&gt;</a>" in html


def test_language_prefix_follows_current_language(glossary_seeded, phase3_open):
    html = _render('{% glossary_link "nulla_osta" %}', lang="ar")
    assert 'href="/ar/glossaire/nulla_osta/"' in html


def test_plain_text_when_gate_closed(glossary_seeded):
    assert _render('{% glossary_link "codice_fiscale" %}') == "codice fiscale"
    assert _render('{% glossary_link "codice_fiscale" "code fiscal" %}') == "code fiscal"
    assert _render('{% glossary_term_url "codice_fiscale" %}') == ""


def test_plain_text_for_unknown_or_unpublished_terms(glossary_seeded, phase3_open):
    assert _render('{% glossary_link "unknown_key" %}') == "unknown key"
    Term.objects.get(key="codice_fiscale").__class__.objects.filter(key="codice_fiscale").update(
        status=PublicationStatus.DRAFT
    )
    from glossary.services import invalidate_link_map

    invalidate_link_map()
    assert _render('{% glossary_link "codice_fiscale" %}') == "codice fiscale"
    assert _render('{% glossary_term_url "nulla_osta" %}') == "/fr/glossaire/nulla_osta/"
