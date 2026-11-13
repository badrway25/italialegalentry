"""
A new version of a rule is new text, and it must not inherit what it has not earned.

Two defects lived here, and both were found by RUNNING the code rather than reading it.

`new_version` did not carry `provenance`. A second version of a rule inherited from the previous
platform quietly became `drafted_from_source` — it acquired the authority of a text drafted from
the norm simply by being edited. That is precisely the laundering the field exists to prevent, and
any edit at all was enough to do it.

`rules_activate_demonstration --undo` only retired. `RETIRED` is terminal, so the flag was one-way:
sixteen retired rules, nothing left to activate, and no way back short of rebuilding the database.
"""

from __future__ import annotations

import datetime as dt

import pytest

from rules import services
from rules.models import LegalRule, LegalSource, ReviewStatus, RuleEffect, RuleProvenance

pytestmark = pytest.mark.django_db


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create_user(
        email="version-author@example.test", password="Local-Only-2026!", full_name="Autrice"
    )


@pytest.fixture
def reviewer(django_user_model):
    return django_user_model.objects.create_user(
        email="version-reviewer@example.test", password="Local-Only-2026!", full_name="Revisore"
    )


@pytest.fixture
def verified_source():
    return LegalSource.objects.create(
        key="src-version",
        title_fr="Travail salarié",
        reference="D.Lgs. 286/1998, art. 22",
        authority="Repubblica Italiana",
        url="https://www.normattiva.it/example",
        consulted_on=dt.date(2026, 9, 21),
        consulted_by="Referente giuridico",
    )


def _rule(author, provenance, source=None, rule_id="R-VER-001"):
    rule = LegalRule.objects.create(
        rule_id=rule_id,
        version=1,
        pathway="salaried_work",
        condition={},
        effect=RuleEffect.WARNING,
        message_key="rules.version",
        message_fr="Un avertissement.",
        valid_from=dt.date(2026, 1, 1),
        provenance=provenance,
        created_by=author,
    )
    if source is not None:
        rule.sources.set([source])
    return rule


@pytest.mark.parametrize(
    ("provenance", "expected_status"),
    [
        (RuleProvenance.LEGACY_PLATFORM, ReviewStatus.LEGACY_CANDIDATE),
        (RuleProvenance.LEGACY_DERIVED, ReviewStatus.LEGACY_CANDIDATE),
        (RuleProvenance.DRAFTED_FROM_SOURCE, ReviewStatus.DRAFT),
    ],
)
def test_a_new_version_keeps_its_provenance_and_restarts_where_it_belongs(
    author, verified_source, provenance, expected_status
):
    original = _rule(author, provenance, verified_source)
    fresh = services.new_version(original, actor=author)

    assert fresh.version == 2
    assert fresh.provenance == provenance, "the new version laundered its provenance"
    assert fresh.review_status == expected_status
    assert list(fresh.sources.all()) == [verified_source]

    original.refresh_from_db()
    assert original.version == 1, "the original was edited instead of superseded"


def test_a_new_version_of_inherited_content_still_cannot_skip_the_chain(
    author, reviewer, verified_source
):
    """
    The point of restarting at LEGACY_CANDIDATE rather than DRAFT.

    From DRAFT the only edge is SOURCE_VERIFIED, which an inherited rule would reach the same way —
    so this looks cosmetic until you ask what the STATE tells a reviewer opening the queue. It says
    the text came from the previous platform, which is the one thing they need to know before
    deciding how hard to look.
    """
    original = _rule(author, RuleProvenance.LEGACY_PLATFORM, verified_source)
    fresh = services.new_version(original, actor=author)

    with pytest.raises(services.TransitionRefused):
        services.transition(fresh, ReviewStatus.LEGAL_REVIEW, actor=reviewer)

    services.transition(fresh, ReviewStatus.SOURCE_VERIFIED, actor=reviewer)
    services.transition(fresh, ReviewStatus.LEGAL_REVIEW, actor=reviewer)
    fresh.refresh_from_db()
    assert fresh.review_status == ReviewStatus.LEGAL_REVIEW
    assert fresh.provenance == RuleProvenance.LEGACY_PLATFORM


def test_a_new_version_carries_no_approval_from_the_old_one(author, reviewer, verified_source):
    """The old approval was of the old text. Carrying it over would approve something unread."""
    original = _rule(author, RuleProvenance.DRAFTED_FROM_SOURCE, verified_source)
    for target in (
        ReviewStatus.SOURCE_VERIFIED,
        ReviewStatus.LEGAL_REVIEW,
        ReviewStatus.APPROVED,
        ReviewStatus.ACTIVE,
    ):
        services.transition(original, target, actor=reviewer)
    assert original.approved_by_label

    fresh = services.new_version(original, actor=author)
    assert fresh.approved_by_label == ""
    assert fresh.approved_by is None
    assert fresh.approved_at is None
    assert not fresh.is_in_force(dt.date(2026, 6, 1))


def test_retiring_then_reopening_is_the_way_back_from_a_terminal_state(
    author, reviewer, verified_source
):
    """
    `RETIRED` goes nowhere, and that is correct: a rule leaves service by being retired, so the
    assessments that used it stay explainable. The way forward is a NEW VERSION, not an edge out of
    a terminal state — which is what `rules_activate_demonstration --undo` now does, after shipping
    once as a one-way trip.
    """
    original = _rule(author, RuleProvenance.LEGACY_DERIVED, verified_source)
    for target in (
        ReviewStatus.SOURCE_VERIFIED,
        ReviewStatus.LEGAL_REVIEW,
        ReviewStatus.APPROVED,
        ReviewStatus.ACTIVE,
        ReviewStatus.RETIRED,
    ):
        services.transition(original, target, actor=reviewer)

    with pytest.raises(services.TransitionRefused):
        services.transition(original, ReviewStatus.ACTIVE, actor=reviewer)

    fresh = services.new_version(original, actor=author)
    assert fresh.review_status == ReviewStatus.LEGACY_CANDIDATE
    assert fresh.version == 2

    for target in (
        ReviewStatus.SOURCE_VERIFIED,
        ReviewStatus.LEGAL_REVIEW,
        ReviewStatus.APPROVED,
        ReviewStatus.ACTIVE,
    ):
        services.transition(fresh, target, actor=reviewer)
    fresh.refresh_from_db()
    assert fresh.is_in_force(dt.date(2026, 6, 1))

    original.refresh_from_db()
    assert original.review_status == ReviewStatus.RETIRED, "the retired version was resurrected"
