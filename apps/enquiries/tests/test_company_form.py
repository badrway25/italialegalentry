"""« Recueil des besoins » form: prescribed labels, order, consent, anti-spam, normalisation."""

import pytest
from django.utils import translation

from cms import locked_content
from cms.forbidden import scan
from enquiries.forms import CompanyNeedsForm
from enquiries.models import CompanyNeedsRequest
from enquiries.tests.conftest import company_payload, honeypot

pytestmark = pytest.mark.django_db

EXPECTED_ORDER = [
    "company_name",
    "sector",
    "headquarters",
    "contact_name_and_role",
    "email",
    "phone",
    "profiles_needed",
    "indicative_headcount",
    "qualifications_required",
    "experience_required",
    "language_requirements",
    "training_needs",
    "indicative_timeline",
    "notes",
]


def test_field_order_and_labels():
    locked_labels = locked_content.get("p1.companies.form.fields", "fr")[0]
    with translation.override("fr"):
        form = CompanyNeedsForm()
        fields = list(form.prescribed_fields())
    assert [bf.name for bf in fields] == EXPECTED_ORDER
    assert [str(bf.label) for bf in fields] == locked_labels
    assert len(fields) == 14
    # the model itself carries the prescribed labels (back-office / exports)
    model_labels = [str(CompanyNeedsRequest._meta.get_field(n).verbose_name) for n in EXPECTED_ORDER]
    assert model_labels == locked_labels


@pytest.mark.parametrize("lang", ["it", "en", "ar"])
def test_labels_fallback_to_french_with_lang_marker(lang):
    with translation.override(lang):
        form = CompanyNeedsForm()
        first = form["company_name"]
        assert str(first.label) == locked_content.get("p1.companies.form.fields", "fr")[0][0]
        assert first.field.label_lang == "fr"
        assert form.fields["consent"].label_lang == "fr"


def test_consent_required_and_text():
    with translation.override("fr"):
        form = CompanyNeedsForm()
    consent = form.fields["consent"]
    assert consent.required is True
    assert consent.initial is False
    assert str(consent.label) == locked_content.text("p1.companies.form.consent", "fr")
    assert "checked" not in str(form["consent"])
    bound = CompanyNeedsForm(honeypot(company_payload(consent="")))
    assert not bound.is_valid()
    assert "consent" in bound.errors


def test_valid_payload_is_valid_and_not_spam():
    form = CompanyNeedsForm(honeypot(company_payload()))
    assert form.is_valid(), form.errors
    assert form.is_spam is False
    assert form.normalised_email() == "maria.rossi@example.test"


def test_honeypot_and_time_trap_flag_spam():
    assert CompanyNeedsForm(honeypot(company_payload(), website_url="http://spam.example")).is_spam is True
    assert CompanyNeedsForm(honeypot(company_payload(), started_seconds_ago=1)).is_spam is True
    assert CompanyNeedsForm(company_payload()).is_spam is True  # no timestamp at all


def test_required_and_optional_fields():
    form = CompanyNeedsForm(honeypot(company_payload(company_name="", sector="", email="", profiles_needed="")))
    assert not form.is_valid()
    for name in ("company_name", "sector", "email", "profiles_needed"):
        assert name in form.errors
    for name in ("phone", "indicative_headcount", "notes", "indicative_timeline"):
        assert name not in form.errors


def test_normalisation_strips_control_characters_and_collapses_spaces():
    # NUL bytes are rejected by Django's ProhibitNullCharactersValidator; other control chars are stripped.
    form = CompanyNeedsForm(honeypot(company_payload(company_name="  ACME \x07  S.p.A.  ", notes="a\tb   c")))
    assert form.is_valid(), form.errors
    assert form.cleaned_data["company_name"] == "ACME S.p.A."
    assert form.cleaned_data["notes"] == "a b c"


def test_max_length_enforced():
    form = CompanyNeedsForm(honeypot(company_payload(profiles_needed="x" * 5000)))
    assert not form.is_valid()
    assert "profiles_needed" in form.errors


def test_no_candidate_fields_and_no_forbidden_wording():
    names = [f.name for f in CompanyNeedsRequest._meta.fields]
    for forbidden in ("candidate", "applicant", "positions", "recruit", "slots"):
        assert not any(forbidden in n for n in names), forbidden
    with translation.override("fr"):
        html = str(CompanyNeedsForm())
    assert scan(html) == []
