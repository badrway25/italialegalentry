"""
The chain the directive asks for: LEGACY_CANDIDATE → SOURCE_VERIFIED → LEGAL_REVIEW → APPROVED →
ACTIVE, and the two things that used to be possible and must not be.

**A rule in force with no approver.** Eleven were seeded that way, on purpose, so the engine could
be demonstrated before the legal review existed. It was documented and a command listed them, and
both of those are weaker than they sound: a rule in force binds somebody, and a list is a thing
you have to remember to read. The database now refuses the row.

**A jurist reviewing sources nobody opened.** All fifteen seeded sources carried an exact
reference and not one carried a consultation date, a name, or a URL. `SOURCE_VERIFIED` exists so
that the step has to happen before a review can claim to rest on it.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.core.exceptions import PermissionDenied, ValidationError
from django.db import IntegrityError, transaction

from rules import services
from rules.models import (
    ALLOWED_REVIEW_TRANSITIONS,
    LegalRule,
    LegalSource,
    ReviewStatus,
    RuleEffect,
    RuleProvenance,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create_user(
        email="chain-editor@example.test", password="Local-Only-2026!", full_name="Redattrice"
    )


@pytest.fixture
def approver(django_user_model):
    return django_user_model.objects.create_user(
        email="chain-approver@example.test", password="Local-Only-2026!", full_name="Revisore"
    )


@pytest.fixture
def unverified_source():
    return LegalSource.objects.create(
        key="src-unverified",
        title_fr="Texte unique",
        reference="D.Lgs. 286/1998, art. 22",
        authority="Repubblica Italiana",
    )


@pytest.fixture
def verified_source():
    return LegalSource.objects.create(
        key="src-verified",
        title_fr="Texte unique",
        reference="D.Lgs. 286/1998, art. 29",
        authority="Repubblica Italiana",
        url="https://www.normattiva.it/example",
        consulted_on=dt.date(2026, 9, 21),
        consulted_by="Referente giuridico",
    )


def _rule(author, *, provenance=RuleProvenance.DRAFTED_FROM_SOURCE, status=ReviewStatus.DRAFT, **extra):
    return LegalRule.objects.create(
        rule_id=extra.pop("rule_id", "R-TEST-001"),
        version=1,
        pathway="salaried_work",
        condition={},
        effect=RuleEffect.WARNING,
        message_key="rules.test",
        message_fr="Un avertissement.",
        valid_from=dt.date(2026, 1, 1),
        review_status=status,
        provenance=provenance,
        created_by=author,
        **extra,
    )


# ---- the chain ---------------------------------------------------------------------------------
def test_the_declared_chain_is_the_one_the_directive_asks_for():
    """Read as a graph, not as five separate assertions: a missing edge is a skippable step."""
    assert ALLOWED_REVIEW_TRANSITIONS[ReviewStatus.LEGACY_CANDIDATE] == frozenset(
        {ReviewStatus.SOURCE_VERIFIED, ReviewStatus.DRAFT}
    )
    assert ALLOWED_REVIEW_TRANSITIONS[ReviewStatus.DRAFT] == frozenset({ReviewStatus.SOURCE_VERIFIED})
    assert ALLOWED_REVIEW_TRANSITIONS[ReviewStatus.SOURCE_VERIFIED] == frozenset(
        {ReviewStatus.LEGAL_REVIEW, ReviewStatus.DRAFT}
    )
    assert ReviewStatus.APPROVED in ALLOWED_REVIEW_TRANSITIONS[ReviewStatus.LEGAL_REVIEW]
    assert ALLOWED_REVIEW_TRANSITIONS[ReviewStatus.APPROVED] >= {ReviewStatus.ACTIVE}
    assert ALLOWED_REVIEW_TRANSITIONS[ReviewStatus.RETIRED] == frozenset()

    # The edge that would make the whole thing decorative.
    assert ReviewStatus.LEGAL_REVIEW not in ALLOWED_REVIEW_TRANSITIONS[ReviewStatus.DRAFT]
    assert ReviewStatus.ACTIVE not in ALLOWED_REVIEW_TRANSITIONS[ReviewStatus.LEGAL_REVIEW]


def test_a_legacy_candidate_cannot_jump_to_legal_review(author, approver, verified_source):
    rule = _rule(author, provenance=RuleProvenance.LEGACY_DERIVED, status=ReviewStatus.LEGACY_CANDIDATE)
    rule.sources.set([verified_source])
    with pytest.raises(services.TransitionRefused):
        services.transition(rule, ReviewStatus.LEGAL_REVIEW, actor=approver)


def test_the_whole_chain_walks_when_every_step_is_satisfied(author, approver, verified_source):
    rule = _rule(author, provenance=RuleProvenance.LEGACY_PLATFORM, status=ReviewStatus.LEGACY_CANDIDATE)
    rule.sources.set([verified_source])

    for target in (
        ReviewStatus.SOURCE_VERIFIED,
        ReviewStatus.LEGAL_REVIEW,
        ReviewStatus.APPROVED,
        ReviewStatus.ACTIVE,
    ):
        services.transition(rule, target, actor=approver)

    rule.refresh_from_db()
    assert rule.review_status == ReviewStatus.ACTIVE
    assert rule.approved_by == approver
    assert rule.approved_by_label == "Revisore"
    assert rule.is_in_force(dt.date(2026, 6, 1))


# ---- source verification -----------------------------------------------------------------------
def test_a_rule_on_an_unverified_source_cannot_be_marked_verified(author, approver, unverified_source):
    """The reference is exact and the source has still never been opened. That is the whole point."""
    rule = _rule(author)
    rule.sources.set([unverified_source])
    with pytest.raises(services.TransitionRefused) as exc:
        services.transition(rule, ReviewStatus.SOURCE_VERIFIED, actor=approver)
    assert "D.Lgs. 286/1998, art. 22" in str(exc.value)


def test_a_date_without_a_name_is_not_a_verification(author, approver, unverified_source):
    unverified_source.consulted_on = dt.date(2026, 9, 21)
    unverified_source.save()
    rule = _rule(author)
    rule.sources.set([unverified_source])
    with pytest.raises(services.TransitionRefused):
        services.transition(rule, ReviewStatus.SOURCE_VERIFIED, actor=approver)

    unverified_source.consulted_by = "Referente giuridico"
    unverified_source.save()
    services.transition(rule, ReviewStatus.SOURCE_VERIFIED, actor=approver)
    rule.refresh_from_db()
    assert rule.review_status == ReviewStatus.SOURCE_VERIFIED


def test_a_rule_with_no_source_at_all_cannot_be_verified(author, approver):
    rule = _rule(author)
    with pytest.raises(services.TransitionRefused):
        services.transition(rule, ReviewStatus.SOURCE_VERIFIED, actor=approver)


# ---- the approver ------------------------------------------------------------------------------
def test_the_database_refuses_an_active_rule_with_no_approver_label(author):
    """
    Not the service: the DATABASE.

    The service already refused this. The seed bypassed the service by writing the status column,
    and eleven rules in force were the result. A domain rule only the service applies is a rule the
    next writer bypasses without noticing.
    """
    rule = _rule(author)
    with pytest.raises(IntegrityError), transaction.atomic():
        LegalRule.objects.filter(pk=rule.pk).update(review_status=ReviewStatus.ACTIVE)


def test_the_database_refuses_an_approved_rule_with_no_approver_label(author):
    rule = _rule(author)
    with pytest.raises(IntegrityError), transaction.atomic():
        LegalRule.objects.filter(pk=rule.pk).update(review_status=ReviewStatus.APPROVED)


def test_clean_says_the_same_thing_the_constraint_does(author):
    """A form should refuse before the database does, with a sentence rather than an IntegrityError."""
    rule = _rule(author)
    rule.review_status = ReviewStatus.ACTIVE
    with pytest.raises(ValidationError) as exc:
        rule.clean()
    assert "review_status" in exc.value.message_dict


def test_an_author_still_cannot_approve_their_own_rule(author, verified_source):
    rule = _rule(author)
    rule.sources.set([verified_source])
    services.transition(rule, ReviewStatus.SOURCE_VERIFIED, actor=author)
    services.transition(rule, ReviewStatus.LEGAL_REVIEW, actor=author)
    with pytest.raises(PermissionDenied):
        services.transition(rule, ReviewStatus.APPROVED, actor=author)


def test_sending_a_rule_back_withdraws_the_approval_with_it(author, approver, verified_source):
    """
    Otherwise a later activation inherits an approval of a text that has since changed.

    APPROVED → DRAFT is a declared edge, so this is reachable by an ordinary reviewer, not a
    contrived state.
    """
    rule = _rule(author)
    rule.sources.set([verified_source])
    for target in (ReviewStatus.SOURCE_VERIFIED, ReviewStatus.LEGAL_REVIEW, ReviewStatus.APPROVED):
        services.transition(rule, target, actor=approver)
    assert rule.approved_by_label

    services.transition(rule, ReviewStatus.DRAFT, actor=approver)
    rule.refresh_from_db()
    assert rule.approved_by_label == ""
    assert rule.approved_by is None
    assert rule.approved_at is None


# ---- what a result carries ---------------------------------------------------------------------
def test_the_snapshot_carries_provenance_and_the_approver(author, approver, verified_source):
    """
    An assessment must be able to say on whose authority, not only what the rule said.

    A result produced by the demonstration ruleset carries a label saying no jurist approved it,
    and it carries it into the stored snapshot — so it survives being read months later by somebody
    who was not there.
    """
    rule = _rule(author, provenance=RuleProvenance.LEGACY_DERIVED)
    rule.sources.set([verified_source])
    for target in (
        ReviewStatus.SOURCE_VERIFIED,
        ReviewStatus.LEGAL_REVIEW,
        ReviewStatus.APPROVED,
        ReviewStatus.ACTIVE,
    ):
        services.transition(rule, target, actor=approver, approver_label="DIMOSTRAZIONE — nessun giurista")

    snapshot = rule.as_snapshot()
    assert snapshot["provenance"] == RuleProvenance.LEGACY_DERIVED
    assert snapshot["approved_by"] == "DIMOSTRAZIONE — nessun giurista"
    assert snapshot["approved_at"]
    assert snapshot["sources"][0]["consulted_on"] == "2026-09-21"
    assert snapshot["sources"][0]["consulted_by"] == "Referente giuridico"
    assert snapshot["sources"][0]["jurisdiction"] == "IT"
