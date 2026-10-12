"""
The domain rules of a need, stated as tests.

The first group is the one that matters most: there is no age criterion in this model, and there is
no way to put one in. Five job openings out of five on the previous platform carried an age band
(20–45, 21–48, 28–55, 24–50, 22–45) as a structured criterion next to the diploma and the years of
experience. That is direct age discrimination under Directive 2000/78/EC and D.lgs. 216/2003, and
the previous-platform audit (part 2 §3, private register) is explicit that the field must not be
migrated.
"""

from __future__ import annotations

import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone

from companies.models import (
    ALLOWED_TRANSITIONS,
    STATE_MODIFIERS,
    CompanyNeed,
    NeedSkill,
    NeedStatus,
    SkillLevel,
    validate_no_age_criterion,
)

pytestmark = pytest.mark.django_db


# ---------------------------------------------------------------------------------------------
# No age criterion — in any form, in any language
# ---------------------------------------------------------------------------------------------
#: WHOLE words, never substrings: « engagement » and « language » both contain "age" and neither is
#: an age criterion. The tokens are compared against the words of the field name and of its label.
NO_AGE_FIELD_TOKENS = frozenset(
    {"age", "âge", "ages", "âges", "eta", "età", "birth", "birthdate", "naissance", "nascita", "dob"}
)


def test_no_field_of_this_app_carries_an_age_criterion() -> None:
    """Field names AND verbose names: a criterion renamed is still the criterion."""
    import re

    from django.apps import apps as django_apps

    offenders = []
    for model in django_apps.get_app_config("companies").get_models():
        for field in model._meta.get_fields():
            name = getattr(field, "name", "")
            verbose = str(getattr(field, "verbose_name", "") or "")
            words = set(re.split(r"[^\wÀ-ɏ]+", f"{name} {verbose}".lower())) - {""}
            words |= set(name.lower().split("_"))
            if words & NO_AGE_FIELD_TOKENS:
                offenders.append(f"{model.__name__}.{name} ({verbose})")
    assert offenders == [], f"an age-shaped field appeared in companies: {offenders}"


@pytest.mark.parametrize(
    "text",
    [
        "20-45",
        "Manœuvre polyvalent 24–50",
        "Âge requis : 21 à 48 ans",
        "Age 22-45",
        "Candidats de moins de 35 ans, âge maximum",
        "Età 28-55",
        "العمر 25",
    ],
)
def test_an_age_criterion_is_refused(text: str) -> None:
    with pytest.raises(ValidationError):
        validate_no_age_criterion(text)


@pytest.mark.parametrize(
    "text",
    [
        "",
        "Soudeur TIG/MIG",
        "3 à 5 ans d’expérience en chantier",
        "1 à 3 ans sur ligne de production",
        "Conduite d’engins, stage de sécurité obligatoire",
        "Apprentissage du vocabulaire technique",
        "Habilitation électrique BT, 2 ans minimum",
    ],
)
def test_a_legitimate_requirement_passes(text: str) -> None:
    validate_no_age_criterion(text)


def test_a_need_refuses_an_age_band_typed_into_its_duties(company, need_factory) -> None:
    need = need_factory(company)
    need.duties = "Conduite d’engins. Profil recherché : 24-50."
    with pytest.raises(ValidationError):
        need.full_clean()


def test_a_skill_refuses_an_age_criterion(company, need_factory) -> None:
    need = need_factory(company)
    skill = NeedSkill(need=need, label="Âge 25 à 40", level=SkillLevel.MANDATORY)
    with pytest.raises(ValidationError):
        skill.full_clean()


# ---------------------------------------------------------------------------------------------
# The need itself
# ---------------------------------------------------------------------------------------------
def test_a_reference_is_allocated_and_is_not_sequential(company, need_factory) -> None:
    """A reference must not disclose how many needs the platform holds."""
    rows = [need_factory(company, title=f"Besoin {index}") for index in range(12)]
    references = [row.reference for row in rows]
    assert all(references)
    assert len(set(references)) == len(references)
    assert all(reference.startswith("B") and len(reference) == 10 for reference in references)
    # A sequential reference would sort exactly like the primary keys; this one does not. Twelve
    # rows make an accidental match one chance in 12! — about two in a billion. (The earlier
    # assertion, « the reference does not end with the primary key », failed once every sixteen
    # runs on a single-digit key: a flaky test is a test that does not test anything.)
    assert references != sorted(references)


def test_a_company_manages_several_needs(company, need_factory) -> None:
    """REQ-B2B-04 — several needs, independently."""
    for i in range(3):
        need_factory(company, title=f"Besoin {i}")
    assert CompanyNeed.objects.filter(company=company).count() == 3


def test_completeness_names_exactly_what_is_missing(company, need_factory) -> None:
    need = need_factory(company, complete=False, title="Besoin incomplet")
    missing = need.missing_for_submission()
    assert need.is_complete is False
    assert any("territoire" in item for item in missing)
    assert any("secteur" in item for item in missing)
    assert any("compétence obligatoire" in item for item in missing)


def test_a_complete_need_is_complete(company, need_factory) -> None:
    need = need_factory(company)
    assert need.missing_for_submission() == []
    assert need.is_complete is True


def test_every_state_carries_a_word_and_a_declared_modifier() -> None:
    """No colour ever carries a state on its own: every state has a word and a declared rule."""
    for value, label in NeedStatus.choices:
        assert str(label).strip(), value
        assert value in STATE_MODIFIERS, value


def test_no_state_can_be_read_as_an_approval() -> None:
    """There is no « approuvé », no « éligible », no « retenu » — this platform approves nobody."""
    forbidden = ("approuv", "éligib", "eligib", "retenu", "sélectionn", "selezionat", "ammess")
    for _value, label in NeedStatus.choices:
        lowered = str(label).lower()
        assert not any(token in lowered for token in forbidden), label


def test_the_transition_table_is_closed() -> None:
    """Every declared target is a declared state, and the terminal states are terminal."""
    for source, targets in ALLOWED_TRANSITIONS.items():
        assert source in NeedStatus.values
        for target in targets:
            assert target in NeedStatus.values
    assert ALLOWED_TRANSITIONS[NeedStatus.CLOSED] == frozenset()
    assert ALLOWED_TRANSITIONS[NeedStatus.WITHDRAWN] == frozenset()


def test_a_hold_without_a_reason_is_invalid(company, need_factory) -> None:
    need = need_factory(company)
    need.status = NeedStatus.ON_HOLD
    with pytest.raises(ValidationError):
        need.full_clean()


# ---------------------------------------------------------------------------------------------
# Verification is read from accounts, never decided here
# ---------------------------------------------------------------------------------------------
def test_verification_state_comes_from_accounts(company_factory) -> None:
    from accounts.models import VerificationStatus

    verified, _user = company_factory("gamma", verified=True)
    pending, _other = company_factory("delta", verified=False)
    assert verified.is_verified is True
    assert verified.verification_status == VerificationStatus.APPROVED
    assert pending.is_verified is False
    assert pending.verification_status == VerificationStatus.PENDING


def test_a_company_without_any_verification_row_is_not_verified(company, superuser) -> None:
    from accounts.models import AccountVerification

    AccountVerification.objects.filter(user__memberships__organisation=company.organisation).delete()
    assert company.is_verified is False


def test_a_verification_granted_for_another_declared_type_does_not_verify_the_company(company_factory) -> None:
    """
    An approval decides ONE declared type. ``accounts.AccountVerification`` is one row per account,
    so an account approved as a PROFESSIONAL carries an APPROVED row; if this company read that row
    it would be verified without anyone ever having verified the legal entity — and it would then
    be allowed to transmit, which is the gate REQ-B2B-01 exists to hold.
    """
    from accounts.models import AccountType, AccountVerification, VerificationStatus

    profile, user = company_factory("epsilon", verified=False)
    row = AccountVerification.objects.get(user=user)
    row.declared_type = AccountType.PROFESSIONAL
    row.status = VerificationStatus.APPROVED
    row.decided_at = timezone.now()
    row.save()

    profile.refresh_from_db()
    assert profile.is_verified is False


# ---------------------------------------------------------------------------------------------
# The motivation of a need (REQ-B2B-02 « motivazione »), and the taxonomy in the reading language
# ---------------------------------------------------------------------------------------------
def test_the_motivation_explains_the_need_and_still_refuses_an_age_criterion(company, need_factory) -> None:
    need = need_factory(company)
    need.motivation = "Deux départs en retraite et une troisième ligne mise en service."
    need.full_clean(exclude=["reference"])

    need.motivation = "Remplacement d’un départ, personne de 24-50 ans."
    with pytest.raises(ValidationError):
        need.full_clean(exclude=["reference"])


def test_a_taxonomy_row_reads_in_the_language_of_the_page(sector) -> None:
    """The Italian labels are seeded and editable; before this they reached no screen."""
    from django.utils import translation

    sector.label_it = "Edilizia e opere pubbliche"
    sector.save(update_fields=["label_it"])
    with translation.override("it"):
        assert sector.label == "Edilizia e opere pubbliche"
    with translation.override("fr"):
        assert sector.label == sector.label_fr
    # No Italian label: the French source, never an empty cell.
    sector.label_it = ""
    with translation.override("it"):
        assert sector.label == sector.label_fr
