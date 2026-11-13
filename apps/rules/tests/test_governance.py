"""
The governance of a legal rule: versions, four eyes, validity windows, reproducibility.

What is being defended here is the difference between a rule engine and a spreadsheet of
if-statements: an outcome must name the rules that produced it, those rules must name a source, a
human other than the author must have approved them, and the whole thing must be replayable after
the rules have moved on.
"""

from __future__ import annotations

import datetime as dt

import pytest
from django.core.exceptions import PermissionDenied, ValidationError

from rules import services
from rules.models import LegalRule, LegalSource, ReviewStatus, RuleEffect

pytestmark = pytest.mark.django_db


@pytest.fixture
def source(db):
    """
    A source that has actually been opened.

    `consulted_on` and `consulted_by` are not decoration here: `SOURCE_VERIFIED` refuses a rule
    whose sources carry a reference and nothing else, which is the state all fifteen seeded
    sources were in. A fixture without them would make every test in this file fail at the first
    step for a reason that has nothing to do with what the test is about.
    """
    return LegalSource.objects.create(
        key="tui-art-22",
        title_fr="Travail salarié",
        reference="D.Lgs. 286/1998, art. 22",
        authority="Repubblica Italiana",
        url="https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:decreto.legislativo:1998-07-25;286",
        consulted_on=dt.date(2026, 9, 21),
        consulted_by="Referente giuridico",
    )


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create_user(email="author@example.test", password="x")


@pytest.fixture
def reviewer(django_user_model):
    return django_user_model.objects.create_user(email="reviewer@example.test", password="x")


def make_rule(author, source=None, **kwargs) -> LegalRule:
    defaults = {
        "rule_id": "R-TEST-001",
        "version": 1,
        "pathway": "salaried_work",
        "condition": {},
        "effect": RuleEffect.MISSING_REQUIREMENT,
        "message_key": "rules.test",
        "message_fr": "Un document est exigé.",
        "requirement_fr": "Passeport en cours de validité.",
        "responsible_actor": "person",
        "valid_from": dt.date(2026, 1, 1),
        "created_by": author,
    }
    defaults.update(kwargs)
    rule = LegalRule.objects.create(**defaults)
    if source is not None:
        rule.sources.add(source)
    return rule


def to_review(rule, actor):
    """
    Walk a rule to the review queue through the declared chain.

    DRAFT no longer leads straight to LEGAL_REVIEW: `SOURCE_VERIFIED` sits between them, because a
    jurist was being handed references that nobody had opened. Centralised here so that adding a
    step to the chain is one edit, not thirty.
    """
    services.transition(rule, ReviewStatus.SOURCE_VERIFIED, actor=actor)
    return services.transition(rule, ReviewStatus.LEGAL_REVIEW, actor=actor)


class TestFourEyes:
    def test_the_author_cannot_approve_their_own_rule(self, author, source):
        rule = make_rule(author, source)
        to_review(rule, author)
        with pytest.raises(PermissionDenied):
            services.transition(rule, ReviewStatus.APPROVED, actor=author)
        rule.refresh_from_db()
        assert rule.review_status == ReviewStatus.LEGAL_REVIEW

    def test_a_different_reviewer_can_approve(self, author, reviewer, source):
        rule = make_rule(author, source)
        to_review(rule, author)
        services.transition(rule, ReviewStatus.APPROVED, actor=reviewer)
        rule.refresh_from_db()
        assert rule.review_status == ReviewStatus.APPROVED
        assert rule.approved_by == reviewer
        assert rule.approved_at is not None

    def test_approval_requires_an_identified_reviewer(self, author, source):
        rule = make_rule(author, source)
        to_review(rule, author)
        with pytest.raises(ValidationError):
            services.transition(rule, ReviewStatus.APPROVED, actor=None)

    def test_sending_back_to_draft_clears_the_approval(self, author, reviewer, source):
        rule = make_rule(author, source)
        to_review(rule, author)
        services.transition(rule, ReviewStatus.APPROVED, actor=reviewer)
        services.transition(rule, ReviewStatus.DRAFT, actor=reviewer)
        rule.refresh_from_db()
        assert rule.approved_by is None and rule.approved_at is None


class TestTransitions:
    def test_an_undeclared_transition_is_refused(self, author, source):
        rule = make_rule(author, source)
        with pytest.raises(ValidationError):
            services.transition(rule, ReviewStatus.ACTIVE, actor=author)

    def test_a_retired_rule_goes_nowhere(self, author, reviewer, source):
        rule = make_rule(author, source)
        to_review(rule, author)
        services.transition(rule, ReviewStatus.APPROVED, actor=reviewer)
        services.transition(rule, ReviewStatus.ACTIVE, actor=reviewer)
        services.transition(rule, ReviewStatus.RETIRED, actor=reviewer)
        rule.refresh_from_db()
        assert rule.retired_at is not None
        with pytest.raises(ValidationError):
            services.transition(rule, ReviewStatus.ACTIVE, actor=reviewer)

    def test_an_unknown_target_state_is_refused(self, author, source):
        rule = make_rule(author, source)
        with pytest.raises(ValidationError):
            services.transition(rule, "en_vigueur_peut_etre", actor=author)

    def test_transitioning_to_the_current_state_is_a_no_op(self, author, source):
        rule = make_rule(author, source)
        assert services.transition(rule, ReviewStatus.DRAFT, actor=author).review_status == ReviewStatus.DRAFT

    def test_every_transition_is_audited(self, author, reviewer, source):
        from audit.models import AuditEvent

        rule = make_rule(author, source)
        to_review(rule, author)
        services.transition(rule, ReviewStatus.APPROVED, actor=reviewer)
        events = AuditEvent.objects.filter(action="rule.transition")
        assert events.count() == 3
        assert {event.metadata["to"] for event in events} == {
            ReviewStatus.SOURCE_VERIFIED,
            ReviewStatus.LEGAL_REVIEW,
            ReviewStatus.APPROVED,
        }
        # The audit says where the content came from, not only where the rule went. Whether a step
        # was taken on inherited material or on material drafted from the norm is the question
        # somebody re-reading this trail in a year will actually have.
        assert {event.metadata["provenance"] for event in events} == {"drafted_from_source"}


class TestARuleCannotBindWithoutASource:
    def test_a_rule_with_no_source_is_refused_before_it_reaches_a_reviewer(self, author, reviewer):
        """
        The refusal moved EARLIER, which is the stronger guarantee.

        It used to fire at activation: a sourceless rule could be drafted, sent to review and
        approved, and only then be refused — so a jurist could spend time approving something the
        system was always going to reject. `SOURCE_VERIFIED` stops it at the first step.

        Asserted on the REFUSAL and on the state, not on a word in the message: that message is a
        translated string, and it began reading « source » in French the day the catalogues were
        filled. A test that depends on the reader's language is a test that breaks on translation.
        """
        rule = make_rule(author, source=None)
        with pytest.raises(ValidationError):
            services.transition(rule, ReviewStatus.SOURCE_VERIFIED, actor=author)
        rule.refresh_from_db()
        assert rule.review_status == ReviewStatus.DRAFT

        # And the step after it is unreachable too, so nothing routes around the first refusal.
        with pytest.raises(ValidationError):
            services.transition(rule, ReviewStatus.LEGAL_REVIEW, actor=author)

    def test_activation_with_a_source_succeeds(self, author, reviewer, source):
        rule = make_rule(author, source)
        to_review(rule, author)
        services.transition(rule, ReviewStatus.APPROVED, actor=reviewer)
        services.transition(rule, ReviewStatus.ACTIVE, actor=reviewer)
        rule.refresh_from_db()
        assert rule.review_status == ReviewStatus.ACTIVE


class TestValidity:
    """The assessment's date decides which rules apply, never today's date."""

    def _activate(self, rule, author, reviewer):
        to_review(rule, author)
        services.transition(rule, ReviewStatus.APPROVED, actor=reviewer)
        services.transition(rule, ReviewStatus.ACTIVE, actor=reviewer)
        return rule

    def test_a_rule_is_not_in_force_before_its_start_date(self, author, reviewer, source):
        rule = self._activate(make_rule(author, source, valid_from=dt.date(2026, 6, 1)), author, reviewer)
        assert rule.is_in_force(dt.date(2026, 5, 31)) is False
        assert rule.is_in_force(dt.date(2026, 6, 1)) is True

    def test_a_rule_is_not_in_force_after_its_end_date(self, author, reviewer, source):
        rule = self._activate(
            make_rule(author, source, valid_from=dt.date(2026, 1, 1), valid_to=dt.date(2026, 6, 30)),
            author,
            reviewer,
        )
        assert rule.is_in_force(dt.date(2026, 6, 30)) is True
        assert rule.is_in_force(dt.date(2026, 7, 1)) is False

    def test_an_old_assessment_selects_the_rules_of_its_own_day(self, author, reviewer, source):
        self._activate(
            make_rule(author, source, rule_id="R-OLD", valid_from=dt.date(2026, 1, 1), valid_to=dt.date(2026, 6, 30)),
            author,
            reviewer,
        )
        self._activate(
            make_rule(author, source, rule_id="R-NEW", valid_from=dt.date(2026, 7, 1)),
            author,
            reviewer,
        )
        in_june = services.evaluate({}, pathway="salaried_work", on_date=dt.date(2026, 6, 15))
        in_august = services.evaluate({}, pathway="salaried_work", on_date=dt.date(2026, 8, 15))
        assert [f.rule_id for f in in_june.findings] == ["R-OLD"]
        assert [f.rule_id for f in in_august.findings] == ["R-NEW"]

    def test_the_end_of_validity_cannot_precede_its_start(self, author):
        rule = LegalRule(
            rule_id="R-BAD",
            version=1,
            pathway="salaried_work",
            effect=RuleEffect.WARNING,
            message_key="k",
            message_fr="m",
            valid_from=dt.date(2026, 6, 1),
            valid_to=dt.date(2026, 1, 1),
        )
        with pytest.raises(ValidationError):
            rule.full_clean()


class TestVersions:
    def test_a_new_version_leaves_the_one_in_force_untouched(self, author, reviewer, source):
        rule = make_rule(author, source)
        to_review(rule, author)
        services.transition(rule, ReviewStatus.APPROVED, actor=reviewer)
        services.transition(rule, ReviewStatus.ACTIVE, actor=reviewer)

        draft = services.new_version(rule, actor=author, message_fr="Un autre document est exigé.")
        rule.refresh_from_db()
        assert draft.version == 2
        assert draft.review_status == ReviewStatus.DRAFT
        assert rule.review_status == ReviewStatus.ACTIVE
        assert rule.message_fr == "Un document est exigé."

    def test_a_new_version_inherits_the_sources(self, author, source):
        rule = make_rule(author, source)
        draft = services.new_version(rule, actor=author)
        assert list(draft.sources.all()) == [source]

    def test_two_versions_of_a_rule_cannot_share_a_number(self, author, source):
        make_rule(author, source)
        with pytest.raises(Exception):  # noqa: B017 - the DB constraint, whatever it surfaces as
            make_rule(author, source)

    def test_only_the_highest_version_in_force_fires(self, author, reviewer, source):
        first = make_rule(author, source)
        to_review(first, author)
        services.transition(first, ReviewStatus.APPROVED, actor=reviewer)
        services.transition(first, ReviewStatus.ACTIVE, actor=reviewer)

        second = services.new_version(first, actor=author, message_fr="Version deux.")
        second.sources.add(source)
        to_review(second, author)
        services.transition(second, ReviewStatus.APPROVED, actor=reviewer)
        services.transition(second, ReviewStatus.ACTIVE, actor=reviewer)

        evaluation = services.evaluate({}, pathway="salaried_work", on_date=dt.date(2026, 6, 1))
        assert len(evaluation.findings) == 1
        assert evaluation.findings[0].version == 2


class TestEvaluation:
    @pytest.fixture
    def in_force(self, author, reviewer, source):
        def activate(**kwargs):
            rule = make_rule(author, source, **kwargs)
            to_review(rule, author)
            services.transition(rule, ReviewStatus.APPROVED, actor=reviewer)
            services.transition(rule, ReviewStatus.ACTIVE, actor=reviewer)
            return rule

        return activate

    def test_a_draft_rule_never_fires(self, author, source):
        make_rule(author, source)
        assert services.evaluate({}, pathway="salaried_work", on_date=dt.date(2026, 6, 1)).findings == []

    def test_the_strongest_effect_decides_the_outcome(self, in_force):
        in_force(rule_id="R-A", effect=RuleEffect.WARNING)
        in_force(rule_id="R-B", effect=RuleEffect.STOP, requirement_fr="")
        evaluation = services.evaluate({}, pathway="salaried_work", on_date=dt.date(2026, 6, 1))
        assert evaluation.outcome == RuleEffect.STOP
        assert evaluation.is_blocking is True

    def test_a_finding_carries_its_sources(self, in_force, source):
        in_force()
        evaluation = services.evaluate({}, pathway="salaried_work", on_date=dt.date(2026, 6, 1))
        assert evaluation.findings[0].sources[0]["reference"] == source.reference

    def test_the_same_source_behind_two_rules_is_listed_once(self, in_force):
        in_force(rule_id="R-A")
        in_force(rule_id="R-B")
        evaluation = services.evaluate({}, pathway="salaried_work", on_date=dt.date(2026, 6, 1))
        assert len(evaluation.findings) == 2
        assert len(evaluation.sources) == 1

    def test_a_rule_of_another_pathway_does_not_fire(self, in_force):
        in_force(rule_id="R-STUDY", pathway="study_and_training_in_italy")
        assert services.evaluate({}, pathway="salaried_work", on_date=dt.date(2026, 6, 1)).findings == []

    def test_missing_lists_only_the_missing_requirements(self, in_force):
        in_force(rule_id="R-A", effect=RuleEffect.WARNING)
        in_force(rule_id="R-B", effect=RuleEffect.MISSING_REQUIREMENT)
        evaluation = services.evaluate({}, pathway="salaried_work", on_date=dt.date(2026, 6, 1))
        assert [f.rule_id for f in evaluation.missing] == ["R-B"]


class TestReproducibility:
    def test_the_snapshot_replays_to_the_same_outcome_after_the_rule_is_retired(
        self, author, reviewer, source
    ):
        rule = make_rule(author, source, condition={"field": "objective", "op": "eq", "value": "work"})
        to_review(rule, author)
        services.transition(rule, ReviewStatus.APPROVED, actor=reviewer)
        services.transition(rule, ReviewStatus.ACTIVE, actor=reviewer)

        facts = {"objective": "work"}
        evaluation = services.evaluate(facts, pathway="salaried_work", on_date=dt.date(2026, 6, 1))
        assert evaluation.outcome == RuleEffect.MISSING_REQUIREMENT

        services.transition(rule, ReviewStatus.RETIRED, actor=reviewer)
        LegalSource.objects.all().delete()

        # Nothing of the rule is left in the database, and the replay still answers.
        assert services.replay(evaluation.snapshot, facts) == RuleEffect.MISSING_REQUIREMENT
        assert services.evaluate(facts, pathway="salaried_work", on_date=dt.date(2026, 6, 1)).findings == []

    def test_the_snapshot_carries_the_condition_and_the_sources_not_a_reference(
        self, author, reviewer, source
    ):
        rule = make_rule(author, source, condition={"field": "objective", "op": "eq", "value": "work"})
        to_review(rule, author)
        services.transition(rule, ReviewStatus.APPROVED, actor=reviewer)
        services.transition(rule, ReviewStatus.ACTIVE, actor=reviewer)
        snapshot = services.evaluate({}, pathway="salaried_work", on_date=dt.date(2026, 6, 1)).snapshot
        frozen = snapshot["rules"][0]
        assert frozen["condition"] == {"field": "objective", "op": "eq", "value": "work"}
        assert frozen["sources"][0]["reference"] == source.reference

    def test_a_replay_with_different_facts_can_answer_differently(self, author, reviewer, source):
        rule = make_rule(author, source, condition={"field": "objective", "op": "eq", "value": "work"})
        to_review(rule, author)
        services.transition(rule, ReviewStatus.APPROVED, actor=reviewer)
        services.transition(rule, ReviewStatus.ACTIVE, actor=reviewer)
        evaluation = services.evaluate({"objective": "work"}, pathway="salaried_work", on_date=dt.date(2026, 6, 1))
        snapshot = evaluation.snapshot
        assert services.replay(snapshot, {"objective": "study"}) == RuleEffect.POSSIBLE


class TestModelValidation:
    def test_an_invalid_condition_is_refused_when_the_rule_is_saved(self, author):
        rule = LegalRule(
            rule_id="R-BAD-COND",
            version=1,
            pathway="salaried_work",
            condition={"field": "secret", "op": "is_set"},
            effect=RuleEffect.WARNING,
            message_key="k",
            message_fr="m",
            valid_from=dt.date(2026, 1, 1),
        )
        with pytest.raises(ValidationError) as excinfo:
            rule.full_clean()
        assert "condition" in excinfo.value.message_dict

    def test_a_missing_requirement_must_say_what_is_missing(self, author):
        rule = LegalRule(
            rule_id="R-NO-REQ",
            version=1,
            pathway="salaried_work",
            effect=RuleEffect.MISSING_REQUIREMENT,
            message_key="k",
            message_fr="m",
            requirement_fr="",
            valid_from=dt.date(2026, 1, 1),
        )
        with pytest.raises(ValidationError) as excinfo:
            rule.full_clean()
        assert "requirement_fr" in excinfo.value.message_dict

    def test_a_responsible_actor_outside_the_case_file_enumeration_is_refused(self, author):
        rule = LegalRule(
            rule_id="R-BAD-ACTOR",
            version=1,
            pathway="salaried_work",
            effect=RuleEffect.WARNING,
            message_key="k",
            message_fr="m",
            responsible_actor="italy_legal_entry",
            valid_from=dt.date(2026, 1, 1),
        )
        with pytest.raises(ValidationError) as excinfo:
            rule.full_clean()
        assert "responsible_actor" in excinfo.value.message_dict

    def test_a_source_renders_a_citation_with_its_consultation_date(self, source):
        source.consulted_on = dt.date(2026, 9, 1)
        source.save()
        citation = source.as_citation()
        assert citation["reference"] == "D.Lgs. 286/1998, art. 22"
        assert citation["consulted_on"] == "2026-09-01"


class TestTheDisplayedText:
    """
    `message_key` exists so the text a person reads lives in the translation system. Nothing read it,
    so every rule message rendered in French whatever the page's language.
    """

    def test_the_french_source_is_used_when_the_key_has_no_translation(self):
        from rules.services import displayed

        assert displayed("rules.work.offer", "Un employeur est requis.") == "Un employeur est requis."

    def test_a_key_never_reaches_the_reader(self):
        """gettext returns the key when there is no entry: `rules.work.offer` on screen is worse."""
        from rules.services import displayed

        assert displayed("rules.nothing.here", "Texte source") == "Texte source"

    def test_an_empty_key_falls_back_without_calling_gettext(self):
        from rules.services import displayed

        assert displayed("", "Texte source") == "Texte source"

    def test_a_real_translation_wins(self, monkeypatch):
        from rules import services

        monkeypatch.setattr(services, "gettext", lambda key: "Un datore di lavoro è richiesto.")
        assert services.displayed("rules.work.offer", "Un employeur est requis.") == (
            "Un datore di lavoro è richiesto."
        )

    def test_the_finding_carries_the_displayed_text(self, author, reviewer, source):
        rule = make_rule(author, source, message_fr="Un document est exigé.", message_key="rules.doc.passport")
        to_review(rule, author)
        services.transition(rule, ReviewStatus.APPROVED, actor=reviewer)
        services.transition(rule, ReviewStatus.ACTIVE, actor=reviewer)
        evaluation = services.evaluate({}, pathway="salaried_work", on_date=dt.date(2026, 6, 1))
        assert evaluation.findings[0].message == "Un document est exigé."
