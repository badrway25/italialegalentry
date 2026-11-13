"""
V5.16 §3 — the forms' legal-basis UX (docs/compliance/FORMS_LEGAL_BASIS_UX.md).

* No box on any public or platform form is pre-ticked.
* A required box in the TEAM's own wording asks for no «consent»: it is an acknowledgement («J’ai lu …»), whose
  error never says «consent» either (category A: processing necessary to answer the request or provide the service).
* The only required boxes that say «consent» are the implementation document's prescribed sentences, kept verbatim:
  the two marked LOCKED COPY — LEGAL REVIEW REQUIRED (company needs, Forum registration; their forms depend on
  Allegato 1 and stay closed) and the newsletter's, a real optional consent on a form of its own (category B).
* Optional choices are separate, unticked and not required.
"""

from __future__ import annotations

import pytest
from django import forms

from cms import locked_content
from consents.models import ConsentPurpose
from consents.services import (
    ACKNOWLEDGEMENT_PURPOSES,
    LOCKED_CONSENT_KEYS,
    LOCKED_COPY_LEGAL_REVIEW_REQUIRED,
    UI_CONSENT_TEXTS,
    ensure_consent_text,
    record_consent,
)
from core.forms import AcknowledgementBooleanField, ConsentBooleanField

LOCKED_SENTENCES = {locked_content.text(key, "fr") for key in LOCKED_CONSENT_KEYS.values()}
CONSENT_WORDS = ("consens", "consent", "acconsent", "موافق")


def _forms(user):
    from accounts.forms import SignupForm
    from community.forms import JoinForm
    from companies.forms import CompanyNeedForm, CompanyProfileForm
    from documents.forms import DocumentUploadForm
    from enquiries.forms import CollaborationProposalForm, CompanyNeedsForm, ContactForm
    from forum.forms import ForumRegistrationForm
    from helpdesk.forms import OpenRequestForm
    from news.forms import NewsletterForm

    return {
        "signup": SignupForm(),
        "community_join": JoinForm(consent_text=UI_CONSENT_TEXTS[ConsentPurpose.COMMUNITY]),
        "company_needs": CompanyNeedsForm(),
        "institution_proposal": CollaborationProposalForm(purpose=ConsentPurpose.INSTITUTION_PROPOSAL),
        "university_proposal": CollaborationProposalForm(purpose=ConsentPurpose.UNIVERSITY_PROPOSAL),
        "contact": ContactForm(),
        "forum_registration": ForumRegistrationForm(),
        "newsletter": NewsletterForm(),
        "documents_upload": DocumentUploadForm(user=user),
        "helpdesk_request": OpenRequestForm(person=None),
        "company_profile": CompanyProfileForm(),
        "company_need": CompanyNeedForm(),
    }


@pytest.fixture
def every_form(db, user_factory, seeded):
    return _forms(user_factory("forms-v516@example.test"))


def _boxes(form):
    return {name: field for name, field in form.fields.items() if isinstance(field, forms.BooleanField)}


def test_no_box_on_any_form_is_pre_ticked(every_form):
    for form_name, form in every_form.items():
        for name, field in _boxes(form).items():
            assert not field.initial, (form_name, name)
            assert not form.initial.get(name), (form_name, name)
            html = str(form[name])
            assert " checked" not in html, (form_name, name, html)


def test_a_required_box_in_the_teams_wording_never_asks_for_consent(every_form):
    for form_name, form in every_form.items():
        for name, field in _boxes(form).items():
            if not field.required:
                continue
            label = str(field.label)
            if label in LOCKED_SENTENCES:
                continue  # prescribed verbatim: checked below
            assert isinstance(field, AcknowledgementBooleanField), (form_name, name)
            assert not any(word in label.lower() for word in CONSENT_WORDS), (form_name, label)
            assert label.startswith("J’ai lu"), (form_name, label)
            error = str(field.error_messages["required"]).lower()
            assert not any(word in error for word in CONSENT_WORDS), (form_name, error)


def test_the_only_consent_sentences_are_the_prescribed_ones_and_each_is_classified(every_form):
    prescribed = {}
    for form_name, form in every_form.items():
        for name, field in _boxes(form).items():
            if str(field.label) in LOCKED_SENTENCES:
                assert isinstance(field, ConsentBooleanField), (form_name, name)
                prescribed[form_name] = str(field.label)
    assert set(prescribed) == {"company_needs", "forum_registration", "newsletter"}
    # A: the two that found required processing on consent are marked for the legal review, never reworded
    assert prescribed["company_needs"] == locked_content.text(
        LOCKED_COPY_LEGAL_REVIEW_REQUIRED[ConsentPurpose.COMPANY_NEEDS], "fr"
    )
    assert prescribed["forum_registration"] == locked_content.text(
        LOCKED_COPY_LEGAL_REVIEW_REQUIRED[ConsentPurpose.FORUM_REGISTRATION], "fr"
    )
    # B: the newsletter's consent is a real optional purpose, on a form that does nothing else
    assert ConsentPurpose.NEWSLETTER not in LOCKED_COPY_LEGAL_REVIEW_REQUIRED
    newsletter = every_form["newsletter"]
    visible = [name for name, field in newsletter.fields.items() if not field.widget.is_hidden]
    assert set(visible) <= {"email", "consent", "website_url"}, visible


def test_optional_choices_are_separate_unticked_and_not_required(every_form):
    join = every_form["community_join"]
    for name in ("show_name", "show_organisation"):
        field = join.fields[name]
        assert isinstance(field, forms.BooleanField) and not isinstance(field, ConsentBooleanField)
        assert field.required is False and not field.initial
    assert join.fields["consent"].required is True
    assert "show_name" not in str(join.fields["consent"].label)


def test_a_bundled_consent_is_not_offered_anywhere(every_form):
    """One box, one purpose: no team label joins a consent to anything else («… et je consens …»)."""
    for form_name, form in every_form.items():
        for name, field in _boxes(form).items():
            label = str(field.label)
            if label in LOCKED_SENTENCES:
                continue
            assert " et je consens" not in label and " and I consent" not in label, (form_name, name)


@pytest.mark.django_db
def test_the_earlier_reused_consent_text_is_versioned_to_the_acknowledgement():
    from consents.models import ConsentText

    old = ConsentText.objects.create(
        purpose=ConsentPurpose.CONTACT,
        language="fr",
        version=1,
        text=locked_content.text("p1.companies.form.consent", "fr"),
        locked_key="p1.companies.form.consent",
        source="locked:p1.companies.form.consent",
    )
    row = ensure_consent_text(ConsentPurpose.CONTACT)
    old.refresh_from_db()
    assert row.version == 2 and row.is_current and row.locked_key == ""
    assert row.text == UI_CONSENT_TEXTS[ConsentPurpose.CONTACT]
    assert old.is_current is False, "the records that point at v1 keep the text the person saw"
    assert ensure_consent_text(ConsentPurpose.CONTACT) == row, "idempotent"
    assert set(ACKNOWLEDGEMENT_PURPOSES) <= set(UI_CONSENT_TEXTS)


@pytest.mark.django_db
def test_a_submission_on_a_database_that_still_holds_the_reused_consent_records_the_acknowledgement():
    """Between migrate and seed_all (or on an old dev / preview database) the v1 reuse is still current."""
    from consents.models import ConsentText

    old = ConsentText.objects.create(
        purpose=ConsentPurpose.INSTITUTION_PROPOSAL,
        language="fr",
        version=1,
        text=locked_content.text("p1.companies.form.consent", "fr"),
        locked_key="p1.companies.form.consent",
        source="locked:p1.companies.form.consent",
    )
    record = record_consent(None, ConsentPurpose.INSTITUTION_PROPOSAL, "qa@example.test", language="fr")
    old.refresh_from_db()
    assert record.consent_text_id != old.pk and old.is_current is False
    assert record.consent_text.text == UI_CONSENT_TEXTS[ConsentPurpose.INSTITUTION_PROPOSAL]
    assert record.consent_text.version == 2 and record.consent_text.locked_key == ""
